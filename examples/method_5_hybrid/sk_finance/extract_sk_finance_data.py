import json, html, re, csv, sys
from pathlib import Path

raw = Path("sk.txt").read_text()
  decoded = bytes(raw, "utf-8").decode("unicode_escape")
  key = '"allBranchData":['
  start = decoded.index(key) + len(key) - 1

  depth = 0
  end = None
  for i in range(start, len(decoded)):
      if decoded[i] == "[":
          depth += 1
      elif decoded[i] == "]":
          depth -= 1
          if depth == 0:
              end = i
              break
  if end is None:
      raise RuntimeError("allBranchData array not terminated")

  data = json.loads(decoded[start:end+1])

  def clean_addr(raw_addr: str) -> str:
      text = html.unescape(raw_addr)
      text = re.sub(r"<[^>]+>", " ", text)
      text = text.replace("\\n", " ").replace("\\", "")
      text = text.replace('"', "")
      return re.sub(r"\s+", " ", text).strip()

  writer = csv.writer(sys.stdout)
  writer.writerow(["state", "city", "branch", "address", "latitude", "longitude"])
  for item in data:
      name = item["name"].strip()
      writer.writerow([
          item.get("state", "").strip(),
          name.title(),
          name,
          clean_addr(item.get("address", "")),
          item.get("latitude"),
          item.get("longitude")
      ])
