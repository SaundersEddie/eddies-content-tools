from datetime import date
from pathlib import Path
import json
import re
from openai_facebook_polisher import polish_facebook_draft

CATEGORY_BLURBS = {
    "history": "This is one of those moments where a single event helped shape what came next.",
    "music": "This is one of those music-history moments that still echoes through playlists, radio, record collections, and arguments between music fans.",
    "film": "This is the kind of film-history moment that helped shape what audiences watched, talked about, or expected from the screen.",
    "science": "A good reminder that discovery is usually built one hard-won step at a time.",
    "literature": "Literature has a funny way of outliving its moment, and some works or writers keep finding new readers long after the original date.",
    "technology": "Tech history moves fast, but some milestones still stand out because they changed what people could build, use, or imagine.",
}


CATEGORY_QUESTIONS = {
    "history": "Did you already know this one, or is this a new rabbit hole?",
    "music": "Is this one still in your rotation, or is it more of a music-history footnote for you?",
    "film": "Have you seen this one, or is it going on the watch list?",
    "science": "What scientific discovery or invention still blows your mind?",
    "literature": "Is this one on your shelf, your reading list, or your 'maybe someday' pile?",
    "technology": "What old piece of tech do you think changed the world more than people realize?",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def list_seed_files() -> list[Path]:
    seeds_dir = Path("drafts/seeds")

    if not seeds_dir.exists():
        return []

    return sorted(seeds_dir.glob("*.json"))


def choose_seed_file(seed_files: list[Path]) -> Path | None:
    if not seed_files:
        print("No seed files found.")
        return None

    print("Saved seed files:\n")

    for index, seed_file in enumerate(seed_files, start=1):
        print(f"{index}. {seed_file.name}")

    while True:
        choice = input("\nChoose a seed file number, or press Enter to cancel: ").strip()

        if not choice:
            return None

        if choice.isdigit():
            index = int(choice)

            if 1 <= index <= len(seed_files):
                return seed_files[index - 1]

        print("Invalid choice. Try again.")


def load_seed_file(seed_file: Path) -> dict:
    return json.loads(seed_file.read_text(encoding="utf-8"))


def get_sources(seed_data: dict) -> str:
    wikipedia_links = seed_data.get("wikipedia", [])
    source_lines = []

    for item in wikipedia_links[:3]:
        title = item.get("title", "Source")
        url = item.get("wikipedia", "")

        if url:
            source_lines.append(f"- {title}: {url}")

    if not source_lines:
        source_lines.append("- Source needed.")

    return "\n".join(source_lines)


def build_draft_title(seed_data: dict) -> str:
    year = seed_data.get("year", "Unknown year")
    description = seed_data.get("description", "Untitled event").rstrip(".")

    max_length = 70

    if len(description) > max_length:
        description = description[:max_length].rsplit(" ", 1)[0] + "..."

    return f"On This Day: {description} ({year})"


def build_raw_post_draft(seed_data: dict) -> str:
    year = seed_data.get("year", "Unknown year")
    description = seed_data.get("description", "No description available.").rstrip(".")
    category = seed_data.get("category", "history")

    blurb = CATEGORY_BLURBS.get(
        category,
        "A small piece of history, but one worth remembering.",
    )

    question = CATEGORY_QUESTIONS.get(
        category,
        "What do you think — interesting, surprising, or one you already knew?",
    )

    return f"""On this day in {year}, {description}.

{blurb}

{question}"""


def build_facebook_draft(seed_data: dict, raw_post_draft: str, polished_draft: str) -> str:
    year = seed_data.get("year", "Unknown year")
    category = seed_data.get("category", "history")
    month = seed_data.get("month", "")
    day = seed_data.get("day", "")
    sources = get_sources(seed_data)
    draft_title = build_draft_title(seed_data)

    return f"""# {draft_title}

Status: Draft
Platform: Facebook
Category: {category}
Historical Date: {month}/{day}
Year: {year}

## Raw Factual Draft

{raw_post_draft}

## Final Facebook Post Copy

{polished_draft}

## Review Notes

- Verify the date and event details before posting.
- Check whether the source is strong enough.
- Rewrite the post in your own voice before publishing.
- Review the AI-polished draft before publishing.

## Sources

{sources}
"""


def build_facebook_copy_paste_post(seed_data: dict, polished_draft: str) -> str:
    sources = get_sources(seed_data)

    return f"""{polished_draft}

Sources:
{sources}
"""


def save_facebook_draft(seed_data: dict) -> Path:
    today = date.today().isoformat()
    description = seed_data.get("description", "facebook-draft")
    slug = slugify(description[:80])

    drafts_dir = Path("drafts/facebook")
    drafts_dir.mkdir(parents=True, exist_ok=True)

    review_file = drafts_dir / f"{today}-{slug}.md"
    copy_file = drafts_dir / f"{today}-{slug}-facebook-copy.txt"

    raw_post_draft = build_raw_post_draft(seed_data)

    try:
        polished_draft = polish_facebook_draft(seed_data, raw_post_draft)
    except Exception as error:
        polished_draft = (
            "AI-polished draft could not be generated.\n\n"
            f"Reason: {error}"
        )

    review_file.write_text(
        build_facebook_draft(seed_data, raw_post_draft, polished_draft),
        encoding="utf-8",
    )

    copy_file.write_text(
        build_facebook_copy_paste_post(seed_data, polished_draft),
        encoding="utf-8",
    )

    return copy_file


def main() -> None:
    print("Create Facebook Draft")
    print("---------------------\n")

    seed_files = list_seed_files()
    selected_seed = choose_seed_file(seed_files)

    if not selected_seed:
        print("No seed selected.")
        return

    seed_data = load_seed_file(selected_seed)
    output_file = save_facebook_draft(seed_data)

    print(f"\nFacebook draft created: {output_file}")


if __name__ == "__main__":
    main()
    