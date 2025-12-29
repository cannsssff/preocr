"""Batch processing example for PreOCR."""

from pathlib import Path
from typing import List, Dict, Any

from preocr import needs_ocr


def process_directory(directory: str) -> List[Dict[str, Any]]:
    """
    Process all files in a directory and determine OCR needs.

    Args:
        directory: Path to directory containing files

    Returns:
        List of results for each file
    """
    results = []
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"Directory not found: {directory}")
        return results

    # Common file extensions to check
    extensions = [
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".tiff",
        ".docx",
        ".pptx",
        ".xlsx",
        ".txt",
    ]

    files = []
    for ext in extensions:
        files.extend(dir_path.glob(f"*{ext}"))
        files.extend(dir_path.glob(f"*{ext.upper()}"))

    print(f"Found {len(files)} files to process\n")

    for file_path in files:
        try:
            result = needs_ocr(str(file_path))
            result["file_path"] = str(file_path)
            results.append(result)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return results


def print_summary(results: List[Dict[str, Any]]):
    """Print a summary of processing results."""
    total = len(results)
    needs_ocr_count = sum(1 for r in results if r["needs_ocr"])
    no_ocr_count = total - needs_ocr_count

    print("\n" + "=" * 60)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {total}")
    print(f"Files needing OCR: {needs_ocr_count} ({needs_ocr_count/total*100:.1f}%)")
    print(f"Files ready (no OCR): {no_ocr_count} ({no_ocr_count/total*100:.1f}%)")
    print("\n" + "-" * 60)

    # Group by file type
    by_type = {}
    for result in results:
        file_type = result["file_type"]
        if file_type not in by_type:
            by_type[file_type] = {"total": 0, "needs_ocr": 0}
        by_type[file_type]["total"] += 1
        if result["needs_ocr"]:
            by_type[file_type]["needs_ocr"] += 1

    print("\nBreakdown by file type:")
    for file_type, stats in sorted(by_type.items()):
        pct = stats["needs_ocr"] / stats["total"] * 100
        print(f"  {file_type:12} {stats['total']:3} files, {stats['needs_ocr']:2} need OCR ({pct:5.1f}%)")

    print("\n" + "=" * 60)


def main():
    """Main function for batch processing example."""
    import sys

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."  # Current directory

    print("PreOCR - Batch Processing Example")
    print(f"Processing directory: {directory}\n")

    results = process_directory(directory)

    if results:
        print_summary(results)

        # Show detailed results
        print("\nDetailed Results:")
        print("-" * 60)
        for result in results[:10]:  # Show first 10
            status = "🔍 NEEDS OCR" if result["needs_ocr"] else "✅ READY"
            print(f"{Path(result['file_path']).name:30} {status:15} {result['reason']}")

        if len(results) > 10:
            print(f"\n... and {len(results) - 10} more files")
    else:
        print("No files found to process.")


if __name__ == "__main__":
    main()

