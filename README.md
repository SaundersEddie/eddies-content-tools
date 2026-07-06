# eddies-content-tools

A local content research and drafting toolkit for creating sourced Facebook, LinkedIn, and website content from date-based historical events, releases, and cultural milestones.

The project is currently focused on finding useful "on this day" style content, filtering it by category, selecting a candidate item, and saving the selected source data as a reusable seed file.

This tool is not intended to auto-post content. It is designed to help collect, review, source, and draft content manually before anything is published.

## Current Focus

The first working flow is:

1. Fetch date-based historical event data.
2. Filter events by category.
3. Display matching candidate items.
4. Select one item.
5. Save the selected item as a seed JSON file.

The seed file becomes the source record that can later be used to generate platform-specific drafts.

## Content Types

The tool is intended to support two broad content styles:

- Significant historical events
- Significant releases in history

Examples include:

- Science history
- Music history
- Film history
- Literature history
- Technology history
- General historical events

## Current Categories

The current script supports rough keyword filtering for:

- `music`
- `film`
- `science`
- `literature`
- `technology`
- `history`

The category filter is intentionally simple for now. It uses keyword matching to narrow down date-based event results. This will likely be improved later with stronger data sources and/or AI-based classification.

## Current Features

- Fetches "on this day" event data for a chosen month and day.
- Allows selecting a category.
- Filters candidate events using category keywords.
- Displays matching events with year, description, source link, and matched keywords.
- Allows choosing a result by number.
- Saves the selected result as a JSON seed file under `drafts/seeds/`.

## Project Structure

```text
eddies-content-tools/
  data/
    topics/
  drafts/
    facebook/
    linkedin/
    website/
    seeds/
  src/
    content_tool.py
  templates/
  README.md
```

## Running the Tool

From the project root:

```bash
python3 src/content_tool.py
```

The script will ask for:

- Month
- Day
- Category

It will then fetch matching historical events, display candidate results, and allow one item to be selected and saved as a seed file.

## Seed Files

Selected items are saved as JSON files in:

```text
drafts/seeds/
```

A seed file contains the selected event data, including:

- Month
- Day
- Category
- Year
- Description
- Matched keywords
- Wikipedia/source links

These seed files will later be used to generate platform-specific drafts.

## Planned Features

### Draft Generation

Generate content drafts from saved seed files for:

- Facebook
- LinkedIn
- eddiesaunders.com

### AI-Assisted Drafting

Use OpenAI to turn selected source data into platform-specific draft content.

Planned AI outputs include:

- Conversational Facebook posts
- More reflective LinkedIn posts
- Website/archive notes
- Suggested titles
- Suggested hashtags or tags
- Source-check warnings
- Missing-context warnings

### Better Data Sources

The current version uses date-based historical event data as a starting point.

Possible future sources include:

- Wikimedia/Wikipedia data
- Wikidata
- MusicBrainz for music release metadata
- Film metadata sources
- Book/literature metadata sources

## Platform Goals

### Facebook

Facebook drafts should be:

- Conversational
- Interesting
- Easy to read
- Slightly nostalgic when appropriate
- End with a question or engagement prompt

### LinkedIn

LinkedIn drafts should be:

- More reflective
- Less casual
- Connected to creativity, learning, process, tools, technology, or building useful things
- Avoid corporate cringe

### eddiesaunders.com

Website drafts should be:

- More archival
- Source-aware
- Useful as future notes or reference material
- Tagged and organized for long-term browsing

## Guiding Principles

- Fetch the data first.
- Keep sources.
- Save selected items before generating posts.
- Generate drafts, not final truth.
- Review before publishing.
- Build one brick at a time.

## Current Milestone

The current milestone is complete:

```text
Fetch -> filter -> select -> save seed JSON
```

The next milestone is:

```text
Saved seed JSON -> basic Facebook draft
```

After that, AI-assisted draft generation can be added on top of the saved seed workflow.
