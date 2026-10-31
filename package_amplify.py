import os
import zipfile
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"
DIST_DIR = FRONTEND_DIR / "dist"
OUTPUT_ZIP = ROOT_DIR / "amplify_deploy.zip"

def build_frontend():
    print("--- Step 1/3: Building Frontend Production Bundle ---")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    result = subprocess.run([npm_cmd, "run", "build"], cwd=FRONTEND_DIR, shell=True)
    if result.returncode != 0:
        print("[ERROR] Frontend build failed. Please fix any build errors above.")
        sys.exit(1)
    print("[OK] Frontend build succeeded.")

def ensure_redirects():
    print("--- Step 2/3: Creating AWS Amplify _redirects for SPA routing ---")
    redirects_file = DIST_DIR / "_redirects"
    redirects_content = "/*    /index.html   200\n"
    redirects_file.write_text(redirects_content, encoding="utf-8")
    print(f"[OK] Generated {redirects_file.name}")

def package_zip():
    print(f"--- Step 3/3: Creating AWS Amplify ZIP: {OUTPUT_ZIP.name} ---")
    if not (DIST_DIR / "index.html").exists():
        print(f"[ERROR] {DIST_DIR / 'index.html'} does not exist. Run build first.")
        sys.exit(1)

    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        for root, _, files in os.walk(DIST_DIR):
            for file in files:
                file_path = Path(root) / file
                # Write with relative path inside dist, placing index.html at root of zip!
                rel_path = file_path.relative_to(DIST_DIR)
                zipf.write(file_path, arcname=str(rel_path).replace("\\", "/"))
                file_count += 1

    size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"\n=======================================================")
    print(f" [SUCCESS] AWS Amplify Package Created: {OUTPUT_ZIP.name}")
    print(f" Total Files: {file_count} | Size: {size_mb:.2f} MB")
    print(f" Location:    {OUTPUT_ZIP}")
    print(f"=======================================================")
    print("\nHow to deploy to AWS Amplify:")
    print("1. Open the AWS Amplify Console (https://console.aws.amazon.com/amplify)")
    print("2. Click 'Create new app' -> 'Deploy without Git provider'")
    print("3. Enter your App name (e.g. EduCloud) and Branch name (e.g. main)")
    print(f"4. Drag and drop: {OUTPUT_ZIP.name}")
    print("5. Click 'Save and deploy' - Your site will be live in ~15 seconds!")
    print("=======================================================\n")

if __name__ == "__main__":
    if "--no-build" not in sys.argv:
        build_frontend()
    ensure_redirects()
    package_zip()
