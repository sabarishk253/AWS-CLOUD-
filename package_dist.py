import os
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_ZIP = ROOT_DIR / "educloud_dist.zip"

EXCLUDE_DIRS = {
    ".venv",
    "node_modules",
    "dist",
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".idea",
    ".vscode"
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".db",
    ".sqlite3",
    ".pkl"
}

def create_dist_zip():
    print(f"Creating clean distributable ZIP: {OUTPUT_ZIP.name}...")
    
    # Ensure local_storage has a placeholder
    local_storage_dir = ROOT_DIR / "backend" / "local_storage"
    local_storage_dir.mkdir(parents=True, exist_ok=True)
    gitkeep_file = local_storage_dir / ".gitkeep"
    if not gitkeep_file.exists():
        gitkeep_file.write_text("")

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        for root, dirs, files in os.walk(ROOT_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            # Skip local storage contents except .gitkeep
            rel_root = Path(root).relative_to(ROOT_DIR)
            if "backend" in rel_root.parts and "local_storage" in rel_root.parts:
                files = [f for f in files if f == ".gitkeep"]

            for file in files:
                if file == OUTPUT_ZIP.name or file.endswith(".zip"):
                    continue
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                if ext in EXCLUDE_EXTENSIONS:
                    continue

                rel_path = file_path.relative_to(ROOT_DIR)
                zipf.write(file_path, arcname=str(rel_path))
                file_count += 1

    zip_size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"Successfully created {OUTPUT_ZIP.name} with {file_count} files ({zip_size_mb:.2f} MB).")

if __name__ == "__main__":
    create_dist_zip()
