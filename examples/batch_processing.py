"""Enhanced batch processing example for PreOCR."""

import sys
from pathlib import Path

from preocr.batch import BatchProcessor


def main():
    """Main function for batch processing example."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Batch process files to determine OCR needs using PreOCR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process current directory
  python batch_processing.py

  # Process specific directory
  python batch_processing.py /path/to/documents

  # Process with 8 workers and layout analysis
  python batch_processing.py /path/to/documents --workers 8 --layout-aware

  # Process only PDFs recursively
  python batch_processing.py /path/to/documents --extensions pdf --recursive

  # Resume from previous results
  python batch_processing.py /path/to/documents --resume-from results.json
        """,
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to process (default: current directory)",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel workers (default: CPU count)",
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching (reprocess all files)",
    )

    parser.add_argument(
        "--layout-aware",
        action="store_true",
        help="Perform layout analysis for PDFs (slower but more accurate)",
    )

    parser.add_argument(
        "--page-level",
        action="store_true",
        help="Perform page-level analysis for PDFs",
    )

    parser.add_argument(
        "--extensions",
        nargs="+",
        default=None,
        help="File extensions to process (e.g., pdf png jpg). Default: common formats",
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories recursively",
    )

    parser.add_argument(
        "--min-size",
        type=int,
        default=None,
        help="Minimum file size in bytes",
    )

    parser.add_argument(
        "--max-size",
        type=int,
        default=None,
        help="Maximum file size in bytes",
    )

    parser.add_argument(
        "--resume-from",
        type=str,
        default=None,
        help="Resume from previous results file (JSON)",
    )

    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable progress bar",
    )

    args = parser.parse_args()

    print("PreOCR - Enhanced Batch Processing")
    print("=" * 80)
    print(f"Directory: {args.directory}")
    print(f"Workers: {args.workers or 'auto (CPU count)'}")
    print(f"Caching: {not args.no_cache}")
    print(f"Layout-aware: {args.layout_aware}")
    print(f"Page-level: {args.page_level}")
    print(f"Recursive: {args.recursive}")
    if args.extensions:
        print(f"Extensions: {', '.join(args.extensions)}")
    if args.min_size:
        print(f"Min size: {args.min_size:,} bytes")
    if args.max_size:
        print(f"Max size: {args.max_size:,} bytes")
    if args.resume_from:
        print(f"Resume from: {args.resume_from}")
    print("=" * 80)
    print()

    try:
        # Create processor
        processor = BatchProcessor(
            max_workers=args.workers,
            use_cache=not args.no_cache,
            layout_aware=args.layout_aware,
            page_level=args.page_level,
            extensions=args.extensions,
            min_size=args.min_size,
            max_size=args.max_size,
            recursive=args.recursive,
            resume_from=args.resume_from,
        )

        # Process directory
        results = processor.process_directory(args.directory, progress=not args.no_progress)

        # Print summary
        results.print_summary()

        # Show detailed results (first 10)
        if results.results:
            print("\nDetailed Results (first 10):")
            print("-" * 80)
            for result in results.results[:10]:
                status = "🔍 NEEDS OCR" if result.get("needs_ocr") else "✅ READY"
                file_name = Path(result["file_path"]).name
                reason = result.get("reason", "Unknown")
                
                # Show page information if available
                page_info = ""
                if result.get("page_count"):
                    page_count = result.get("page_count", 0)
                    pages_needing_ocr = result.get("pages_needing_ocr", 0)
                    pages_with_text = result.get("pages_with_text", 0)
                    if page_count > 0:
                        page_info = f" | {page_count} pages ({pages_needing_ocr} need OCR, {pages_with_text} ready)"
                
                print(f"{file_name:40} {status:15} {reason}{page_info}")
                
                # Show page-level details if available
                if result.get("pages"):
                    for page in result["pages"][:5]:  # Show first 5 pages
                        page_num = page.get("page_number", 0)
                        page_needs_ocr = page.get("needs_ocr", False)
                        page_status = "🔍 NEEDS OCR" if page_needs_ocr else "✅ READY"
                        page_reason = page.get("reason", "Unknown")
                        print(f"  └─ Page {page_num:3}: {page_status:15} {page_reason}")
                    if len(result["pages"]) > 5:
                        print(f"  └─ ... and {len(result['pages']) - 5} more pages")

            if len(results.results) > 10:
                print(f"\n... and {len(results.results) - 10} more files")

    except KeyboardInterrupt:
        print("\n\nProcessing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
