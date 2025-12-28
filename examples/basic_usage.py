"""Basic usage example for PreOCR."""

from preocr import needs_ocr


def main():
    """Demonstrate basic PreOCR usage."""
    # Example file paths (replace with your actual files)
    files = [
        "document.pdf",
        "image.png",
        "report.docx",
        "data.txt",
    ]
    
    print("PreOCR - Basic Usage Example\n")
    print("=" * 50)
    
    for file_path in files:
        try:
            result = needs_ocr(file_path)
            
            status = "✅ NO OCR" if not result["needs_ocr"] else "🔍 NEEDS OCR"
            
            print(f"\nFile: {file_path}")
            print(f"Status: {status}")
            print(f"Type: {result['file_type']}")
            print(f"Category: {result['category']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Reason: {result['reason']}")
            
            # Show some signals
            signals = result["signals"]
            if signals.get("text_length", 0) > 0:
                print(f"Text length: {signals['text_length']} characters")
            if signals.get("image_entropy") is not None:
                print(f"Image entropy: {signals['image_entropy']:.2f}")
            
        except FileNotFoundError:
            print(f"\nFile not found: {file_path}")
        except Exception as e:
            print(f"\nError processing {file_path}: {e}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()

