"""Example demonstrating threshold customization with Config."""

from preocr import needs_ocr, BatchProcessor, Config


def main():
    """Demonstrate Config usage for threshold customization."""
    print("PreOCR - Configuration Example\n")
    print("=" * 60)

    # Example 1: Single file with custom config
    print("\n1. Single File with Custom Config")
    print("-" * 60)
    
    # Create stricter config (higher thresholds)
    strict_config = Config(
        min_text_length=100,              # Require 100 chars instead of 50
        min_office_text_length=200,       # Require 200 chars for office docs
        layout_refinement_threshold=0.85, # Lower threshold triggers OpenCV more
    )
    
    print(f"Config: min_text_length={strict_config.min_text_length}, "
          f"min_office_text_length={strict_config.min_office_text_length}")
    
    # Use with needs_ocr
    try:
        result = needs_ocr("document.pdf", config=strict_config)
        print(f"Result: needs_ocr={result['needs_ocr']}, "
              f"confidence={result['confidence']:.2f}")
    except FileNotFoundError:
        print("File not found (this is just an example)")

    # Example 2: Batch processing with custom thresholds
    print("\n2. Batch Processing with Custom Thresholds")
    print("-" * 60)
    
    # Option A: Pass individual parameters
    _processor_a = BatchProcessor(
        min_text_length=75,
        min_office_text_length=150,
        layout_refinement_threshold=0.80,
    )
    print("BatchProcessor created with individual threshold parameters")
    
    # Option B: Use Config object
    custom_config = Config(
        min_text_length=75,
        min_office_text_length=150,
    )
    _processor_b = BatchProcessor(config=custom_config)
    print("BatchProcessor created with Config object")
    
    # Example 3: Comparing default vs custom thresholds
    print("\n3. Comparing Default vs Custom Thresholds")
    print("-" * 60)
    
    default_config = Config()  # Uses all defaults
    lenient_config = Config(
        min_text_length=30,      # Lower threshold (more lenient)
        min_office_text_length=50,
    )
    
    print(f"Default: min_text_length={default_config.min_text_length}")
    print(f"Lenient: min_text_length={lenient_config.min_text_length}")
    print("\nLenient config will flag fewer files as needing OCR")
    
    # Example 4: Domain-specific configuration
    print("\n4. Domain-Specific Configuration")
    print("-" * 60)
    
    # Medical forms might need stricter thresholds
    _medical_config = Config(
        min_text_length=150,  # Medical forms often have sparse text
        min_office_text_length=300,
    )
    
    # Business letters might need lenient thresholds
    _business_config = Config(
        min_text_length=30,   # Business letters usually have good text
        min_office_text_length=50,
    )
    
    print("Medical forms config: stricter thresholds")
    print("Business letters config: lenient thresholds")
    
    print("\n" + "=" * 60)
    print("\nNote: Adjust thresholds based on your validation results!")
    print("See docs/VALIDATION_GUIDE.md for guidance on tuning thresholds.")


if __name__ == "__main__":
    main()

