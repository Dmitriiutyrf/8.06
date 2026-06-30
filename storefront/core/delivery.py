import os
import zipfile

def package_product(product_id, products_root="../products"):
    """Zips the product folder for delivery."""
    product_folder = os.path.join(products_root, product_id)
    os.makedirs("assets", exist_ok=True)
    zip_path = os.path.join("assets", f"{product_id}.zip")

    if not os.path.exists(product_folder):
        return None, f"Product folder not found at {product_folder}"

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(product_folder):
                if any(x in root for x in [".git", "__pycache__"]):
                    continue
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(product_folder))
                    zipf.write(file_path, arcname)
        return zip_path, None
    except Exception as e:
        return None, str(e)
