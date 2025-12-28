"""Entry point for running the full-load pipeline locally.

The script is intentionally minimal: load config, connect to Postgres,
execute staged SQL files in order, and emit basic logging.
"""
import argparse
import logging
import sys
import time
from pathlib import Path

import psycopg2
from psycopg2 import sql

HERE = Path(__file__).parent
ROOT = HERE.parent
SQL_DIR = ROOT / "sql"
DATA_DIR = ROOT / "data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def load_sql_files(batch_id: str):
    ordered_files = [
        "00_init.sql",
        "10_bronze_load.sql",
        "20_silver_build_staging.sql",
        "30_quality_checks.sql",
        "40_atomic_swap.sql",
    ]
    statements = []
    for name in ordered_files:
        path = SQL_DIR / name
        content = path.read_text()
        statements.append((name, content.replace(":batch_id", f"'{batch_id}'")))
    return statements


def run_sql(conn, statements, batch_id: str):
    with conn.cursor() as cur:
        for name, statement in statements:
            logging.info("Running %s", name)
            if name == "10_bronze_load.sql":
                csv_path = DATA_DIR / "provider_device_catalog.csv"
                cur.execute(
                    """
                    CREATE TEMP TABLE tmp_bronze_load (
                        provider_id INTEGER,
                        device_id TEXT,
                        device_name TEXT,
                        device_type TEXT,
                        last_updated TIMESTAMPTZ
                    );
                    """
                )
                copy_stmt = """
                    COPY tmp_bronze_load
                        (provider_id, device_id, device_name, device_type, last_updated)
                    FROM STDIN WITH (FORMAT csv, HEADER true)
                """
                with csv_path.open("r", encoding="utf-8") as infile:
                    cur.copy_expert(copy_stmt, infile)
                cur.execute(
                    """
                    INSERT INTO bronze.provider_device_catalog
                        (provider_id, device_id, device_name, device_type, last_updated, batch_id)
                    SELECT provider_id, device_id, device_name, device_type, last_updated, %s
                    FROM tmp_bronze_load;
                    """,
                    (batch_id,),
                )
                cur.execute("DROP TABLE IF EXISTS tmp_bronze_load;")
            else:
                cur.execute(sql.SQL(statement))
    conn.commit()


def ensure_state_table(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE SCHEMA IF NOT EXISTS metadata;
            CREATE TABLE IF NOT EXISTS metadata.batch_state (
                state_key     TEXT PRIMARY KEY,
                last_batch_id TEXT,
                updated_at    TIMESTAMPTZ DEFAULT NOW()
            );
            """
        )
    conn.commit()


def load_last_batch_id(conn) -> str | None:
    with conn.cursor() as cur:
        cur.execute("SELECT last_batch_id FROM metadata.batch_state WHERE state_key = %s;", ("default",))
        row = cur.fetchone()
        return row[0] if row else None


def save_last_batch_id(conn, batch_id: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO metadata.batch_state (state_key, last_batch_id, updated_at)
            VALUES (%s, %s, NOW())
            ON CONFLICT (state_key)
            DO UPDATE SET last_batch_id = EXCLUDED.last_batch_id, updated_at = NOW();
            """,
            ("default", batch_id),
        )
    conn.commit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch-id",
        help="Identifier for the load batch (default: reuse last run or generate new timestamp)",
    )
    parser.add_argument("--config", default=HERE / "config.yaml", type=Path)
    args = parser.parse_args()

    try:
        import yaml
    except ImportError as exc:
        logging.error("Missing dependency pyyaml: %s", exc)
        sys.exit(1)

    cfg = yaml.safe_load(args.config.read_text())
    conn_info = cfg.get("warehouse", {})

    logging.info("Connecting to warehouse at %s:%s", conn_info.get("host"), conn_info.get("port"))
    conn = psycopg2.connect(
        host=conn_info.get("host"),
        port=conn_info.get("port"),
        user=conn_info.get("user"),
        password=conn_info.get("password"),
        dbname=conn_info.get("database"),
    )

    ensure_state_table(conn)
    batch_id = args.batch_id or load_last_batch_id(conn) or f"batch-{int(time.time())}"
    logging.info("Using batch id: %s", batch_id)

    statements = load_sql_files(batch_id=batch_id)
    run_sql(conn, statements, batch_id=batch_id)
    save_last_batch_id(conn, batch_id)
    logging.info("Full load completed")


if __name__ == "__main__":
    main()
