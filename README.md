The existing README has the right information, but it reads more like development notes than a finished public project page. This version tightens it up, puts setup first, clearly explains that users need their **own OpenAI API key**, and keeps the project scope honest.

I have left one obvious placeholder for your PayPal link because I’m not going to guess where people should send the coffee money. ☕

# Eddie’s Content Tools

A local Python tool for researching date-based events and creating sourced Facebook post drafts.

The tool finds historical and cultural events for a selected date, filters the results by category, saves the selected event and its sources, and uses OpenAI to turn the factual seed into a more natural Facebook post draft.

It does not automatically publish or schedule anything. Every generated post is intended to be reviewed before being copied into Facebook.

Project repository:

[https://github.com/SaundersEddie/eddies-content-tools](https://github.com/SaundersEddie/eddies-content-tools)

Created by Eddie Saunders:

[https://eddiesaunders.com](https://eddiesaunders.com)

## Features

* Fetch date-based historical and cultural events.
* Filter results by category.
* Display matching candidate events.
* Select an event from the results.
* Save the selected event as a JSON seed file.
* Preserve source links for later review.
* Generate a raw factual Facebook draft.
* Use OpenAI to polish the wording.
* Create a structured Markdown review file.
* Create a clean Facebook copy/paste text file.
* Fall back to the raw factual draft if OpenAI polishing fails.

## Current Categories

The current category filters are:

* History
* Music
* Film
* Science
* Literature
* Technology

Category filtering is keyword-based, so results should still be reviewed before use.

## Current Scope

This version is deliberately focused on Facebook drafting.

The following features are not currently included:

* LinkedIn posts
* Website articles
* Post scheduling
* Automatic publishing
* Facebook API integration
* Multi-platform content generation
* Social-media account management

The goal is to keep the Facebook workflow useful and understandable before adding more platforms or automation.

## How It Works

The current workflow is:

1. Enter a month and day.
2. Select a category.
3. Fetch date-based event data.
4. Review matching candidate events.
5. Select one event.
6. Save the event and its sources as a seed JSON file.
7. Generate a raw factual Facebook draft.
8. Send the draft to OpenAI for conversational polishing.
9. Save a review Markdown file.
10. Save a Facebook copy/paste text file.

The generated content should always be treated as a draft rather than final truth.

## Requirements

You will need:

* Python 3.10 or newer
* An internet connection
* Your own OpenAI API key
* An OpenAI API account with available API credit or billing

This project does not include an API key.

Each user must create and pay for their own OpenAI API usage.

OpenAI API keys can be managed here:

[https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

OpenAI API usage is separate from a ChatGPT subscription. Having a ChatGPT account or paid ChatGPT plan does not automatically provide API credit.

## Installation

Clone the repository:

```bash
git clone https://github.com/SaundersEddie/eddies-content-tools.git
```

Move into the project directory:

```bash
cd eddies-content-tools
```

Optional but recommended: create a virtual environment.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

## OpenAI API Key Setup

Create a file named `.env` in the project root.

Add your OpenAI API key using the following variable name:

```env
OPENAI=your_openai_api_key_here
```

The expected environment variable is:

```text
OPENAI
```

Do not place quotation marks around the key unless your local environment specifically requires them.

Do not commit the `.env` file to GitHub or share it publicly.

The project uses `python-dotenv` to load the key locally.

## Running the Tool

Run the menu application from the project root:

```bash
python src/run_content_tool.py
```

Depending on your Python installation, you may need:

```bash
python3 src/run_content_tool.py
```

The menu currently provides the following options:

1. Create a new event seed.
2. Create a Facebook draft from a saved seed.
3. Run the complete seed and draft workflow.
4. Quit.

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

The `.env` file is created locally and should never be committed.

## Seed Files

Selected events are saved as JSON files under:

```text
drafts/seeds/
```

A seed file contains information such as:

* Month
* Day
* Year
* Category
* Event description
* Matched category keywords
* Source titles
* Source links

The seed JSON file acts as the local source-of-truth record for the selected event.

## Generated Facebook Files

Generated drafts are saved under:

```text
drafts/facebook/
```

The tool creates two output files.

### Review Markdown File

The Markdown review file contains:

* Event metadata
* Raw factual draft
* OpenAI processing status
* Review notes
* Final Facebook post copy
* Source links

The final post and its sources are grouped together at the bottom of the document for easy review and copying.

### Facebook Copy/Paste File

The text file contains:

* Final Facebook post copy
* Source links

This provides one simple block that can be reviewed and copied without searching through the full Markdown document.

## OpenAI Polishing

The OpenAI step rewrites the raw factual draft into a more natural Facebook post.

The prompt instructs the model to:

* Keep the event factual.
* Preserve the year and core event.
* Avoid invented details.
* Use conversational language.
* Avoid corporate or LinkedIn-style wording.
* Avoid academic writing.
* Keep the post reasonably short.
* Add a light engagement question when appropriate.
* Return plain text rather than Markdown.
* Avoid placing source links inside the public-facing post text.

If OpenAI polishing fails, the tool uses the raw factual draft as the fallback Facebook copy.

The failure reason is recorded in the Markdown review file.

## Source Handling

Sources are preserved locally so the event can be checked before publication.

The current event provider may return Wikipedia links and related source information. Those links are retained in:

* The seed JSON file
* The Markdown review file
* The Facebook copy/paste text file

Sources should still be evaluated for quality.

A source link being present does not automatically mean every detail in the event description is complete, current, or correct.

## Review Before Publishing

This tool creates drafts, not final truth.

Before publishing, check:

* The event date
* The event year
* Names and spellings
* The factual wording
* Source quality
* Regional release dates
* Whether the event fits the selected category
* Whether the engagement question makes sense
* Whether the finished post sounds like you

Regional differences can be especially important for:

* Album releases
* Song releases
* Film premieres
* Book publication dates
* Product launches
* Technology releases

## Privacy and Security

Your OpenAI API key is loaded from your local `.env` file.

Do not:

* Commit `.env`
* Paste your API key into source files
* Upload your key in screenshots
* Share the key in support requests
* Include the key in generated drafts
* Publish the key in a fork or pull request

If a key is accidentally exposed, revoke it through your OpenAI account and create a new one.

## Known Limitations

* Category filtering is based on keywords.
* Source data may use awkward historical present-tense wording.
* Source results may be incomplete.
* Cultural release dates may vary by country or region.
* AI-polished copy may still contain mistakes.
* The full-flow menu may still require selecting the newly created seed manually.
* The tool does not independently verify every factual claim.
* Generated files must be reviewed before publication.

## Development Status

The core Facebook workflow is operational:

```text
Fetch event
-> Filter by category
-> Select event
-> Save seed JSON
-> Generate factual draft
-> Polish with OpenAI
-> Save review file
-> Save Facebook copy file
```

The project is considered a usable local drafting tool, although category filtering, validation, source presentation, and workflow convenience can still be improved.

## Contributing

Bug reports, suggestions, and improvements are welcome through the GitHub repository:

[https://github.com/SaundersEddie/eddies-content-tools](https://github.com/SaundersEddie/eddies-content-tools)

Please keep proposed changes aligned with the current Facebook-first scope.

Large multi-platform abstractions, automatic publishing systems, and scheduling features are intentionally outside the current project direction.

## Author

Created by Eddie Saunders.

Website:

[https://eddiesaunders.com](https://eddiesaunders.com)

GitHub repository:

[https://github.com/SaundersEddie/eddies-content-tools](https://github.com/SaundersEddie/eddies-content-tools)

## Support the Project

This project is free to use.

If it saves you some time and you would like to buy me a coffee, you can send a small PayPal donation here:

http://paypal.me/edwynsaunders1

No pressure. The code still works without caffeine, although the developer may not.
