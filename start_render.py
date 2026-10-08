import os
import shutil
import sys
from pathlib import Path


def prepare_database():
    app_dir = Path(__file__).resolve().parent
    configured_path = os.environ.get("EPIDEMIA_DB_PATH") or "/var/data/epidemia.db"
    database_path = Path(configured_path).expanduser()
    if not database_path.is_absolute():
        database_path = app_dir / database_path
    database_path = database_path.resolve()
    os.environ["EPIDEMIA_DB_PATH"] = str(database_path)

    if database_path.exists():
        return database_path

    seed_path = app_dir / "epidemia.db"
    if not seed_path.is_file():
        raise FileNotFoundError(f"Database seed file not found: {seed_path}")

    database_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(seed_path, database_path)
    print(f"Initialized persistent database at {database_path}")
    return database_path


def main():
    prepare_database()
    app_path = Path(__file__).resolve().with_name("epidemiaTH.py")
    port = os.environ.get("PORT", "8501")
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.address=0.0.0.0",
        f"--server.port={port}",
    ]
    os.execv(sys.executable, command)


if __name__ == "__main__":
    main()
