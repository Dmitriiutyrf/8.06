import os
import shutil
import zipfile

def package_product(product_id, base_dir=".."):
    """Zips the product folder for delivery."""
    product_folder = os.path.join(base_dir, product_id)
    zip_filename = f"{product_id}.zip"
    zip_path = os.path.join("assets", zip_filename)

    if not os.path.exists(product_folder):
        return None, "Product folder not found."

    # Ensure assets dir exists
    os.makedirs("assets", exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(product_folder):
                # Skip engine/.git and pycache
                if ".git" in root or "__pycache__" in root:
                    continue
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(product_folder))
                    zipf.write(file_path, arcname)
        return zip_path, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    # Test zipping
    path, err = package_product("teamsync_ai")
    if path:
        print(f"Package created: {path}")
    else:
        print(f"Error: {err}")
