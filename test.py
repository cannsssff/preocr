from pathlib import Path
from preocr import needs_ocr

files = list(Path("/home/yuvarajk/Downloads").glob("*.pdf"))
needs_ocr_count = 0
skipped_count = 0

print("="*60)
print(f"Testing {len(files)} PDF files...")
print("="*60)
print()

for file_path in files:
    result = needs_ocr(file_path, layout_aware=True)
    
    status = "🔴 NEEDS OCR" if result["needs_ocr"] else "✅ SKIP OCR"
    print(f"{status} | {file_path.name}")
    print(f"  Confidence: {result['confidence']:.2f}")
    print(f"  Reason: {result['reason']}")
    print(f"  Reason Code: {result['reason_code']}")
    
    # Show layout analysis if available
    if "layout" in result and "opencv" in result["layout"]:
        ocv = result["layout"]["opencv"]
        print(f"  OpenCV: {ocv.get('text_coverage', 0):.1f}% text, "
              f"{ocv.get('text_regions', 0)} regions, "
              f"{ocv.get('layout_type', 'unknown')} layout")
    
    print()
    
    if result["needs_ocr"]:
        needs_ocr_count += 1
    else:
        skipped_count += 1

print("="*60)
print(f"Summary: OCR needed: {needs_ocr_count}, Skipped: {skipped_count}")
print(f"Total files: {len(files)}")
print("="*60)