import sys
import os
import argparse
import shutil
import tarfile
import zipfile

def prepare_toml(platform_name):
    with open("gemini-extension.toml", "r") as f:
        content = f.read()

    if platform_name == "win32":
        # On Windows, we'll use telegram.exe
        # We replace "python src/client.py" with "telegram.exe"
        # Note: We might need ".\telegram.exe" if simple filename fails, 
        # but "telegram.exe" is usually fine if CWD is the dir.
        new_content = content.replace("python src/client.py", "telegram.exe")
    else:
        # On Unix, we need ./telegram
        new_content = content.replace("python src/client.py", "./telegram")

    # Write to dist folder
    os.makedirs("dist", exist_ok=True)
    with open("dist/gemini-extension.toml", "w") as f:
        f.write(new_content)
    
    print(f"Created dist/gemini-extension.toml for {platform_name}")

def create_archives():
    exclude_dirs = {'.git', '.github', '.idea', 'dist', '__pycache__', 'venv', '.venv'}
    base_name = "gemini-cli-telegram-extension"
    
    files_to_archive = []
    for root, dirs, files in os.walk("."):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file == f"{base_name}.zip" or file == f"{base_name}.tar.gz":
                continue
            files_to_archive.append(os.path.join(root, file))

    # Create ZIP
    zip_filename = f"{base_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in files_to_archive:
            zf.write(file, os.path.normpath(file))
    print(f"Created {zip_filename}")

    # Create TAR.GZ
    tar_filename = f"{base_name}.tar.gz"
    with tarfile.open(tar_filename, "w:gz") as tar:
        for file in files_to_archive:
            tar.add(file, arcname=os.path.normpath(file))
    print(f"Created {tar_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare release artifacts.")
    parser.add_argument("platform", nargs="?", help="Target platform for TOML preparation (e.g., win32)")
    parser.add_argument("--archive", action="store_true", help="Create release archives (zip and tar.gz)")
    
    args = parser.parse_args()

    if args.platform:
        prepare_toml(args.platform)
    
    if args.archive:
        create_archives()
    
    if not args.platform and not args.archive:
        parser.print_help()


