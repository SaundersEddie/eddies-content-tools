# eddies-content-tools

Local Python tools for creating sourced Facebook draft posts from date-based historical and cultural events.

This project is currently focused on Facebook-only content drafting.

It does not auto-post, schedule posts, or publish anything. It helps research, save source data, and generate draft copy that can be reviewed before posting manually.

## Current Purpose

`eddies-content-tools` helps create "On This Day" style Facebook drafts based on historical events, music history, film history, literature, science, technology, and other date-driven milestones.

The current workflow is:

1. Fetch date-based event data.
2. Filter events by category.
3. Select an event.
4. Save the selected event as a seed JSON file.
5. Generate a raw factual Facebook draft.
6. Use OpenAI to polish the Facebook post copy.
7. Save:
   - a review Markdown draft
   - a clean Facebook copy/paste text file with sources

## Current Scope

This project is currently Facebook-only.

Out of scope for now:

- LinkedIn posts
- Website posts
- Scheduling
- Auto-posting
- Multi-platform content abstraction
- Social media API publishing

The goal is to make the Facebook draft workflow genuinely useful before expanding the project.

## Project Structure

```text
eddies-content-tools/
├── data/
│   └── topics/
├── drafts/
│   ├── seeds/
│   └── facebook/
├── src/
│   ├── content_tool.py
│   ├── create_facebook_draft.py
│   ├── openai_facebook_polisher.py
│   └── run_content_tool.py
├── templates/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Environment Variables

OpenAI API access is handled with `python-dotenv`.

Create a `.env` file in the project root:

```env
OPENAI=your_openai_api_key_here
```

The `.env` file should not be committed to Git.

Make sure `.env` is included in `.gitignore`.

## Running the Tool

Use the menu runner:

```bash
python src/run_content_tool.py
```

The menu allows you to:

1. Create a new seed from a date and category.
2. Create a Facebook draft from a saved seed.
3. Run the full flow.
4. Quit.

## Output Files

Generated files are saved under:

```text
drafts/facebook/
```

The tool currently creates two output files:

### Review Markdown Draft

A structured `.md` file containing:

- raw factual draft
- AI-polished Facebook copy
- review notes
- sources

### Facebook Copy/Paste File

A clean `.txt` file containing:

- final Facebook post copy
- sources

This file is intended to be copied and pasted directly into Facebook.

## Seed Files

Selected events are saved as JSON seed files under:

```text
drafts/seeds/
```

Seed files are the source-of-truth records for selected events.

They preserve the event data and source references used to generate drafts.

## Categories

Current categories:

- history
- music
- film
- science
- literature
- technology

Each category has its own draft blurb and engagement question style.

## OpenAI Draft Polishing

The OpenAI step takes the raw factual Facebook draft and rewrites it into a more natural Facebook-style post.

The polished draft should:

- stay factual
- preserve the date and year
- avoid invented details
- avoid corporate or LinkedIn tone
- use a conversational Facebook tone
- include a light engagement question when appropriate
- avoid Markdown formatting in the final post copy

The OpenAI-generated post should still be reviewed before publishing.

## Important Notes

This tool creates drafts, not final truth.

Always review:

- event accuracy
- date accuracy
- source quality
- wording
- regional release differences for music, film, books, and similar cultural events

Country and region may matter for release-date-based posts.

## Git Safety

Do not commit:

```text
.env
```

Recommended `.gitignore` entries:

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
.DS_Store
```

## Current Status

Current working milestone:

```text
Fetch event -> filter by category -> select event -> save seed JSON -> generate Facebook draft -> polish with OpenAI -> save review and copy/paste files
```

Next likely improvements:

- automatically use the seed just created in the full-flow menu
- improve source display formatting
- improve category filtering
- add better validation around missing source data
