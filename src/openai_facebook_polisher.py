import os
from dotenv import load_dotenv
from openai import OpenAI


def get_openai_client():
    load_dotenv()

    api_key = os.getenv("OPENAI")

    if not api_key:
        raise RuntimeError(
            "Missing OpenAI API key. Add OPENAI=your_api_key_here to your .env file."
        )

    return OpenAI(api_key=api_key)


def polish_facebook_draft(seed_data, raw_draft):
    """
    Takes the saved seed data and the basic factual draft,
    then returns a Facebook-friendly polished version.
    """

    client = get_openai_client()

    year = seed_data.get("year", "Unknown year")
    event = seed_data.get("text", "")
    category = seed_data.get("category", "history")

    prompt = f"""
You are helping polish a Facebook post draft.

Rules:
- Keep the post factual.
- Do not invent details.
- Preserve the year: {year}
- Preserve the core event: {event}
- Use a conversational Facebook tone.
- Avoid corporate or LinkedIn-style language.
- Avoid academic wording.
- Keep it short.
- Add a light engagement question if appropriate.
- Do not include hashtags unless they are genuinely useful.
- Do not include source links in the public-facing post text.

Category: {category}

Raw draft:
{raw_draft}

Write only the polished Facebook post text.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text.strip()
