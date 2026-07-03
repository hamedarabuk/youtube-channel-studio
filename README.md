# youtube-channel-studio

A Claude Code skill toolkit that helps YouTube creators optimise video metadata and thumbnails. Two skills: a one-time channel foundation interview and a per-video optimisation pipeline. Uses your Claude Code subscription for the AI reasoning. Costs roughly $0.10 to $0.20 per thumbnail generated through OpenAI gpt-image-2.

## Requirements

- [Claude Code](https://www.anthropic.com/claude-code) installed and signed in to your subscription
- Python 3.11 or newer
- OpenAI API key, required only for the thumbnail-image step: get one at https://platform.openai.com/api-keys. Everything else (the interview, the title, description, and copy outputs) runs on your Claude subscription at no extra cost. Without a key, the skill still writes a thumbnail brief you can hand to any image tool by hand.

## Install

1. Clone the repo:
   ```bash
   git clone https://github.com/hamedarabuk/youtube-channel-studio.git
   cd youtube-channel-studio
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   # macOS and Linux:
   source .venv/bin/activate
   # Windows:
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up your API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and paste your `OPENAI_API_KEY`.

## First run, per channel

1. Open the repo in Claude Code from the repo root:
   ```bash
   claude
   ```

2. Invoke the foundation skill. In Claude Code, type:
   > Run the yt-channel-init skill for my channel.

3. Answer the interview. It takes about 15 to 20 minutes and covers identity, niche, audience, voice, visuals, competition, goals, and hard rules.

4. Your foundation lands at `channels/<your-handle>/foundation.md`. The per-video skill reads it as strategic context every time it runs.

## Per video

1. In Claude Code, type:
   > Run the yt-video-optimise skill.

2. Provide the inputs the skill asks for:
   - Current title and description (or "no draft yet")
   - Topic brief in two or three sentences
   - Main character reference image path
   - Three to six video screenshots
   - Optional: three to six competitor thumbnails for this specific video genre

3. Outputs land in `channels/<your-handle>/videos/<date>-<slug>/outputs/`.

## What it produces per video

- `title.txt`: the recommended title
- `title-alternatives.md`: three more title options with rationale
- `description.md`: a full SEO-friendly description with hashtags
- `thumbnail-brief.md`: a structured creative brief for the thumbnail
- `thumbnail.png`: a generated thumbnail at 1792x1024, ready for YouTube upload
- `pinned-comment.txt`: a first comment to pin
- `community-post.txt`: a launch-day Community tab post
- `run.json`: a manifest capturing all inputs and outputs for replay

## Multi-channel support

Run `yt-channel-init` again for each new channel. Each gets its own subdirectory under `channels/`. The per-video skill always asks which channel before it loads the foundation.

## Troubleshooting

- **"OPENAI_API_KEY is not set"**: your `.env` file is missing or the key line is empty. Re-check step 3 of Install; the key must be pasted into `.env`, not `.env.example`.
- **"openai is not installed"**: run `pip install -r requirements.txt` again inside your active virtual environment.
- **Python version errors**: this toolkit needs Python 3.11 or newer. Run `python --version` to check.

## Sharing this repo

Fork or clone. The `channels/` directory is gitignored by default, so your channel data and generated outputs do not ship with the template when you push.

## Licence

MIT.

## Author

Built by Hamed Arab Choobdar with Claude Code.
