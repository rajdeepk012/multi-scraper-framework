import csv
import html
import json
import re
from pathlib import Path

# Path to the embedded data dump
SOURCE_PATH = Path("sk.txt")
# Output CSV path
OUTPUT_PATH = Path("sk_branches.csv")


def extract_branch_array(raw_text: str) -> list:
    """Decode the Next.js payload and pull the allBranchData array."""
    decoded = bytes(raw_text, "utf-8").decode("unicode_escape")
    key = '"allBranchData":['
    start = decoded.index(key) + len(key) - 1  # include the opening bracket

    depth = 0
    end = None
    for idx in range(start, len(decoded)):
        char = decoded[idx]
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
            if depth == 0:
                end = idx
                break
    if end is None:
        raise RuntimeError("Failed to locate the end of allBranchData array")

    array_text = decoded[start : end + 1]
    return json.loads(array_text)


def clean_address(raw_address: str) -> str:
    """Remove HTML tags, escapes, and redundant whitespace from the address."""
    text = html.unescape(raw_address)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\\n", " ")
    text = text.replace("\\", "")
    text = text.replace('"', "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> None:
    raw_text = SOURCE_PATH.read_text()
    branches = extract_branch_array(raw_text)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["state", "city", "branch", "address", "latitude", "longitude"])
        for item in branches:
            name = item.get("name", "").strip()
            writer.writerow([
                item.get("state", "").strip(),
                name.title(),
                name,
                clean_address(item.get("address", "")),
                item.get("latitude"),
                item.get("longitude"),
            ])

    print(f"Wrote {len(branches)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
