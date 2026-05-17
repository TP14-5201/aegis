import os
import argparse
from PIL import Image

def convert_and_delete(target_directory, quality):
    extensions = (".png", ".jpg", ".jpeg")
    
    if not os.path.exists(target_directory):
        print(f"Error: The directory '{target_directory}' does not exist.")
        return

    for root, dirs, files in os.walk(target_directory):
        # Skip wellness folder entirely
        if "wellness" in root.lower():
            continue

        for file in files:
            if file.lower().endswith(extensions):
                if not "icon-" in file.lower():
                    file_path = os.path.join(root, file)
                    name_without_ext = os.path.splitext(file_path)[0]
                    webp_path = f"{name_without_ext}.webp"

                    try:
                        with Image.open(file_path) as img:
                            # Ensure image is in a mode compatible with WebP
                            if img.mode in ("RGBA", "P"):
                                img = img.convert("RGBA")
                            else:
                                img = img.convert("RGB")
                                
                            img.save(webp_path, "webp", quality=quality)
                        
                        if os.path.exists(webp_path):
                            os.remove(file_path)
                            print(f"Converted & Deleted: {file}")
                    
                    except Exception as e:
                        print(f"Failed to process {file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert images to WebP and delete originals.")
    
    # Flag for target directory
    parser.add_argument(
        "--path", 
        type=str, 
        default="../frontend/public/images", 
        help="Target directory to scan (default: frontend/public/images)"
    )
    
    # Flag for quality
    parser.add_argument(
        "--quality", 
        type=int, 
        default=80, 
        help="Compression quality 1-100 (default: 80)"
    )

    args = parser.parse_args()

    # Final confirmation before execution
    print(f"Target Directory: {args.path}")
    print(f"Target Quality:   {args.quality}%")
    confirm = input("This will permanently DELETE original files (any files starting with 'icon-' will be skipped). Proceed? (y/n): ")
    
    if confirm.lower() == 'y':
        convert_and_delete(args.path, args.quality)
        print("Finished.")
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()