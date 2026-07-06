from datetime import date
from pathlib import Path
import json
import re
import urllib.request
import urllib.error
import unicodedata


CATEGORY_KEYWORDS = {
    "music": [
        "album", "song", "single", "band", "singer", "musician", "concert",
        "record", "recorded", "released", "chart", "music"
    ],
    "film": [
        "film", "movie", "cinema", "premiere", "released", "actor",
        "actress", "director"
    ],
    "science": [
        "science", "scientist", "discovered", "discovery", "space",
        "nasa", "physics", "chemistry", "biology", "medicine"
    ],
    "literature": [
        "book", "novel", "poem", "author", "writer", "published",
        "literature"
    ],
    "technology": [
        "computer", "software", "internet", "technology", "launched",
        "programming", "video game", "console"
    ],
    "history": []
}


def fetch_on_this_day(month: int, day: int) -> dict:
    url = f"https://byabbe.se/on-this-day/{month}/{day}/events.json"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "eddies-content-tools/0.1"
        },
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def keyword_matches(text: str, keyword: str) -> bool:
    """
    Match whole words or short phrases only.

    This prevents false matches like:
    - band matching Banda
    - art matching party
    - record matching recorded only when we do not want that
    """
    pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
    return re.search(pattern, text.lower()) is not None


def filter_events(events: list[dict], category: str) -> list[dict]:
    keywords = CATEGORY_KEYWORDS.get(category, [])

    if not keywords:
        return events

    matches = []

    for event in events:
        description = event.get("description", "")
        matched_keywords = [
            keyword for keyword in keywords
            if keyword_matches(description, keyword)
        ]

        if matched_keywords:
            event["_matched_keywords"] = matched_keywords
            matches.append(event)

    return matches

def choose_event(events: list[dict]) -> dict | None:
    if not events:
        print("No matching events to choose from.")
        return None

    while True:
        choice = input("Choose an item number, or press Enter to cancel: ").strip()

        if not choice:
            return None

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(events):
                return events[index - 1]

        print("Invalid choice. Try again.")
        
        
def slugify(text: str) -> str:
    """
    Create a filename-safe slug.
    Converts accented characters where possible.
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def save_seed_file(selected_event: dict, category: str, month: int, day: int) -> Path:
    year = selected_event.get("year", "unknown-year")
    description = selected_event.get("description", "untitled")
    slug = slugify(description[:80])

    seeds_dir = Path("drafts/seeds")
    seeds_dir.mkdir(parents=True, exist_ok=True)

    output_file = seeds_dir / f"{month:02d}-{day:02d}-{category}-{year}-{slug}.json"

    seed_data = {
        "month": month,
        "day": day,
        "category": category,
        "year": year,
        "description": description,
        "matched_keywords": selected_event.get("_matched_keywords", []),
        "wikipedia": selected_event.get("wikipedia", []),
    }

    output_file.write_text(
        json.dumps(seed_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return output_file

def list_seed_files() -> list[Path]:
    seeds_dir = Path("drafts/seeds")

    if not seeds_dir.exists():
        return []

    return sorted(seeds_dir.glob("*.json"))


def choose_seed_file(seed_files: list[Path]) -> Path | None:
    if not seed_files:
        print("No seed files found.")
        return None

    print("\nSaved seed files:")

    for index, seed_file in enumerate(seed_files, start=1):
        print(f"{index}. {seed_file.name}")

    while True:
        choice = input("Choose a seed file number, or press Enter to cancel: ").strip()

        if not choice:
            return None

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(seed_files):
                return seed_files[index - 1]

        print("Invalid choice. Try again.")


def load_seed_file(seed_file: Path) -> dict:
    return json.loads(seed_file.read_text(encoding="utf-8"))


def build_basic_facebook_draft(seed_data: dict) -> str:
    year = seed_data.get("year", "Unknown year")
    description = seed_data.get("description", "No description available.")
    category = seed_data.get("category", "history")
    month = seed_data.get("month")
    day = seed_data.get("day")
    wikipedia = seed_data.get("wikipedia", [])

    source_lines = []

    for item in wikipedia[:3]:
        title = item.get("title", "Source")
        url = item.get("wikipedia", "")

        if url:
            source_lines.append(f"- {title}: {url}")

    if not source_lines:
        source_lines.append("- Source needed.")

    return f"""# Facebook Draft

Status: Draft
Platform: Facebook
Category: {category}
Historical Date: {month}/{day}
Year: {year}

## Post Draft

On this day in {year}:

{description}

A small piece of history, but one worth remembering.

What do you think — interesting, surprising, or one you already knew?

## Sources

{chr(10).join(source_lines)}
"""

def save_facebook_draft(seed_data: dict, seed_file: Path) -> Path:
    today = date.today().isoformat()
    description = seed_data.get("description", "facebook-draft")
    slug = slugify(description[:80])

    drafts_dir = Path("drafts/facebook")
    drafts_dir.mkdir(parents=True, exist_ok=True)

    output_file = drafts_dir / f"{today}-{slug}.md"
    content = build_basic_facebook_draft(seed_data)

    output_file.write_text(content, encoding="utf-8")

    return output_file


def main() -> None:
    print("eddies-content-tools")
    print("---------------------")

    today = date.today()

    month_input = input(f"Month [{today.month}]: ").strip()
    day_input = input(f"Day [{today.day}]: ").strip()

    month = int(month_input) if month_input else today.month
    day = int(day_input) if day_input else today.day

    print("\nCategories:")
    for category_name in CATEGORY_KEYWORDS:
        print(f"- {category_name}")

    category = input("\nCategory [history]: ").strip().lower() or "history"

    try:
        data = fetch_on_this_day(month, day)
    except urllib.error.URLError as error:
        print(f"Could not fetch events: {error}")
        return

    events = data.get("events", [])
    matches = filter_events(events, category)

    print(f"\nFound {len(matches)} matching item(s) for {month}/{day} in {category}.\n")

    visible_matches = matches[:10]

    for index, event in enumerate(visible_matches, start=1):
        year = event.get("year", "Unknown year")
        description = event.get("description", "No description")
        matched_keywords = event.get("_matched_keywords", [])

        print(f"{index}. {year} — {description}")

        if matched_keywords:
            print(f"   Matched: {', '.join(matched_keywords)}")

        wikipedia_links = event.get("wikipedia", [])
        if wikipedia_links:
            first_link = wikipedia_links[0].get("wikipedia")
            if first_link:
                print(f"   Source: {first_link}")

        print()

    selected_event = choose_event(visible_matches)

    if not selected_event:
        print("No item selected.")
        return

    print("\nSelected:")
    print(f"{selected_event.get('year')} — {selected_event.get('description')}")

    seed_file = save_seed_file(selected_event, category, month, day)
    print(f"\nSeed saved: {seed_file}")
            
if __name__ == "__main__":
    main()
    