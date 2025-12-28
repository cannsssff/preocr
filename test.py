from preocr import needs_ocr
import json

# Test with layout_aware=True for better accuracy
result = needs_ocr("/home/yuvarajk/Downloads/ORTHO case 1.pdf", layout_aware=True)

print("="*60)
print("OCR Detection Result")
print("="*60)
print(f"Needs OCR: {result['needs_ocr']}")
print(f"Confidence: {result['confidence']}")
print(f"Reason: {result['reason']}")
print(f"Reason Code: {result['reason_code']}")
print()

if "layout" in result:
    print("Layout Analysis:")
    layout = result["layout"]
    
    # Basic layout (pdfplumber-based)
    print("  Basic Layout (pdfplumber-based):")
    print(f"    Text Coverage: {layout.get('text_coverage', 0)}%")
    print(f"    Image Coverage: {layout.get('image_coverage', 0)}%")
    print(f"    Layout Type: {layout.get('layout_type', 'unknown')}")
    print(f"    Has Images: {layout.get('has_images', False)}")
    if layout.get('text_density', 0) > 0:
        print(f"    Text Density: {layout.get('text_density', 0)}")
    if layout.get('is_mixed_content', False):
        print(f"    Mixed Content: {layout.get('is_mixed_content', False)}")
    
    # OpenCV layout (if available)
    if "opencv" in layout:
        print("\n  OpenCV Analysis (advanced):")
        ocv = layout["opencv"]
        print(f"    Text Coverage: {ocv.get('text_coverage', 0)}%")
        print(f"    Image Coverage: {ocv.get('image_coverage', 0)}%")
        print(f"    Text Regions: {ocv.get('text_regions', 0)}")
        print(f"    Image Regions: {ocv.get('image_regions', 0)}")
        print(f"    Layout Type: {ocv.get('layout_type', 'unknown')}")
        print(f"    Complexity: {ocv.get('layout_complexity', 'unknown')}")
        if ocv.get('total_pages', 0) > 0:
            print(f"    Total Pages: {ocv.get('total_pages', 0)}")
            print(f"    Pages Analyzed: {ocv.get('pages_analyzed', 0)}")
    else:
        print("\n  ⚠️  OpenCV layout analysis not available.")
        print("     Install with: pip install preocr[layout-refinement]")

print("\n" + "="*60)
print("Full Result (JSON):")
print("="*60)
print(json.dumps(result, indent=2, default=str))