---
name: yt-video-optimise
description: >
  Per-video optimisation pipeline. Generates a title (plus 3 alternatives),
  description, thumbnail brief, thumbnail image, pinned comment, and
  community post. Reads the channel foundation for voice, audience, and
  visual rules. Run once per video, before or just after uploading to
  YouTube Studio.
when-to-use: >
  When a video is ready to publish and you want research-backed metadata,
  or when an existing video is underperforming and you want to re-optimise
  its title, description, and thumbnail.
tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Skill body

## Overview for Claude Code

This skill takes a per-video brief from the user and produces six output
files: title, description, thumbnail brief, thumbnail image, pinned comment,
and community post. Every output is grounded in two sources: (1) the channel
foundation file (voice, audience, visual identity, hard rules) and (2) the
2026 YouTube SEO research patterns encoded in this skill body. Read both
before generating anything.

---

## Step 1: Resolve the channel foundation

Ask:

> Which channel is this for? (Paste the handle, e.g. `@SilverForgeStudio`)

Derive the slug the same way yt-channel-init does: strip `@`, lowercase,
hyphens for spaces.

Attempt to read `channels/<slug>/foundation.md` using the Read tool.

If the file does not exist, stop and say:

> No foundation file found for `<handle>`. Please run `yt-channel-init`
> first. It takes about 15 minutes and makes every subsequent optimisation
> significantly more accurate.

If the file exists, read it fully into context. Do not summarise it yet.
Every per-output prompt below will reference specific fields from this file.

---

## Step 2: Collect per-video inputs

Ask all of the following in one message (they are a single logical block):

> I have your channel foundation loaded. Now tell me about this specific
> video.
>
> 1. Current title (or type "no draft" if you have not written one yet).
> 2. Current description (or "no draft").
> 3. Topic brief in 2-3 sentences: what is the video about, what will the
>    viewer get out of it, and why does this topic matter now?
> 4. Path to the main character reference image for this video. This is
>    usually the on-camera person from the foundation file. You can use a
>    fresh expression image if the emotion in this video differs from the
>    default.
> 5. Paths to 3-6 screenshots from the video that show key moments or
>    the setting. (Or paste a YouTube URL if the video is already uploaded.)
> 6. Paths to 3-6 competitor thumbnails for this specific video genre.
>    Optional, but recommended: seeing what performs in your niche sharpens
>    the thumbnail brief considerably. Skip with "none" if you do not have
>    them.

Wait for the user's full reply before proceeding.

---

## Step 3: Create the video directory

From the topic brief and today's date, derive a short video slug:

- Lowercase, hyphens only, max 5 words, no stop words.
- Example: "How I Made a Gold Ring in 3 Hours" becomes `gold-ring-3-hours`.

Date format: YYYY-MM-DD.

Create these paths (using Bash to make the directories, or the Write tool
on first file in each directory):

```
channels/<slug>/videos/<date>-<video-slug>/inputs/
channels/<slug>/videos/<date>-<video-slug>/outputs/
```

Write a `request.md` to `inputs/` capturing:

- Channel slug
- Video slug
- Date
- User's raw inputs (title draft or "no draft", description draft or "no
  draft", topic brief, image paths, competitor thumbnail paths or "none")
- Foundation file path

This file makes the run reproducible and auditable.

---

## Step 4: Generate the six outputs

Work through the six outputs in order. Each has its own rules. Do not
generate them all in one pass: complete each one, write the file, then move
to the next.

### Output 1: Title

**Research rules (all must apply):**
- Front-load the hook in the first 50 characters. Mobile viewers see
  35-40 characters before truncation; the most compelling element must sit
  there.
- Optimal total length: 70-100 characters for search breadth.
- Use one of the proven high-CTR formulas where it fits the topic naturally:
  specific number + outcome ("7 Things That Doubled My Revenue"), transformation
  promise ("How I Went From X to Y"), warning pattern ("Stop Doing This With
  Your Camera"), versus frame ("X vs Y: One Winner Shocked Me"), year-action
  tag ("Best AI Tools 2026 for Creators").
- Curiosity-gap pattern is valid, but the gap must close with real payoff
  inside the video. Do not write a gap you cannot close: it lifts CTR briefly
  but tanks average view duration, which triggers suppression within 24 hours.
- Apply the foundation's banned-phrases list. Apply the foundation's
  must-include phrases if any exist.
- No all-caps. No generic "How To" with no specificity.
- Do not repeat the exact title phrase in the description.

**Primary title:** write the single strongest option.

**Three alternatives:** each must use a genuinely different formula
(number-based, curiosity-gap, how-to, story-hook). Three trivial variants of
one idea are not alternatives. For each, write one sentence explaining which
formula it uses and why it might outperform the primary in a specific context
(e.g. "better for search-intent queries", "better for browse feed on mobile").

Write the primary title to `outputs/title.txt`.
Write the three alternatives and their rationale to `outputs/title-alternatives.md`.

---

### Output 2: Description

**Research rules (all must apply):**
- First sentence: contains the primary keyword and reads as a mini-promise,
  not a topic label. "In this video" is a topic label. "I built an engagement
  ring in one afternoon using only hand tools" is a mini-promise.
- First 150 characters: these appear before the "Show more" fold in search
  and feed previews. They must earn the click independently. Write them as
  if they are the only thing the viewer will read.
- Main body: 200-300 words. Use semantic variation around the topic (related
  terms, synonyms, relevant questions the video answers) rather than
  repeating the primary keyword. YouTube understands topic depth via related
  terms.
- Chapters: if the video is over 10 minutes, or if the user indicated
  chapters are relevant, include timestamps. Ask the user: "Do you want
  chapter markers? If yes, list your chapter titles and timecodes and I'll
  format them." Title chapters like chapter headings, not transcripts
  ("Setup and Settings" not "Me talking about setup").
- CTA: match the foundation's standard CTA pattern exactly.
- Hashtags: 3-5 only, placed at the very bottom of the description after
  all other content. Using more than 15 causes YouTube to ignore all of them.
- End-of-description boilerplate: use the foundation's end-screen and CTA
  pattern for this section.
- Tone: first-person, warm, consistent with the foundation's voice adjectives.
  Use the foundation's locale (British or American English). No em-dashes
  anywhere.
- Do not repeat the exact title phrase as the opening line.

Write to `outputs/description.md`.

---

### Output 3: Thumbnail brief

**Research rules (all must apply):**
- Face presence outperforms object-only by 25-30%. Use the on-camera person
  from the foundation unless the video content genuinely does not feature them.
- Expression: 73% of viewers prefer genuine and relatable over theatrical
  "shocked" faces. Choose an expression that matches the emotional register
  of the topic. High-contrast emotional expressions (curiosity, mild urgency)
  still drive measurable CTR. Avoid expressions that look staged or synthetic.
- Colour: use one complementary colour pair for maximum impact (yellow/violet,
  red/cyan, blue/orange). Contrast ratio above 4.5:1 lifts mobile CTR
  measurably. Refer to the foundation's brand colour palette and find the
  highest-contrast pair within it, or against a background.
- On-image text: 2-3 bold words maximum. Never more than 5. Font must be
  legible at 120x68 pixels (mobile thumbnail size). Do not place text in the
  lower-right corner (YouTube's timestamp overlay covers it). The text should
  grab attention and intrigue, NOT copy the title verbatim. Thumbnail text
  and title text serve different functions: the thumbnail earns the click,
  the title provides context. Redundancy wastes both.
- Composition: rule of thirds. Clear single focal point (face or subject).
  Use leading lines toward the focal point. Visual tension via juxtaposition
  triggers the curiosity gap.
- Avoid: low contrast, dense text, multiple focal points, AI-generated
  artefacts or stock-photo aesthetic (audiences pattern-recognise synthetic
  images and associate them with low-quality content).
- Aspect ratio: 16:9.

Write a structured thumbnail brief as a markdown document to
`outputs/thumbnail-brief.md`. The brief must include these fields:

```
## Subject
[Main character: who, what expression, what they are wearing or holding,
where they are positioned in the frame]

## Background setting
[Location or studio, real or constructed]

## Lighting
[Mood and direction: warm side-light, harsh overhead, soft diffused, etc.]

## Colour palette
[3 dominant colours with hex codes or names, the contrast pair, which colour
is the background vs foreground]

## Focal point
[What the viewer's eye goes to first, and why]

## On-image text
[Exact 2-3 words, font weight, placement, colour, what it must NOT say
(e.g. must not copy the title)]

## Composition notes
[Rule of thirds positioning of the subject, leading lines, any juxtaposition
element that creates visual tension]

## What to avoid
[Specific elements that would break the brief or conflict with the
foundation's visual identity]

## Aspect ratio
16:9 (1792x1024 for generation)
```

If the user provided competitor thumbnails, note what patterns you observed
in them and what this brief consciously borrows from or differs from.

---

### Output 4: Thumbnail image

Synthesise the thumbnail brief into a single, well-constructed prompt for
gpt-image-2. The prompt must:

- Describe subject, expression, setting, lighting, colour palette, and
  on-image text in one paragraph.
- Be specific enough that a generation will match the brief closely.
- Specify the on-image text explicitly (e.g. "bold white sans-serif text
  at the top-left reading 'FIRST TRY'").
- Not exceed one paragraph. Do not include multiple options or parenthetical
  alternatives.

Run the following Bash command from the repo root:

```bash
python scripts/gpt_image_client.py \
  --action generate \
  --prompt "<single-paragraph prompt synthesised from the brief>" \
  --size 1792x1024 \
  --quality high \
  --output channels/<slug>/videos/<date>-<video-slug>/outputs/thumbnail.png
```

The client strips C2PA metadata automatically.

If the command fails (no OPENAI_API_KEY set, network error, or gpt_image_client.py
not found), report the error clearly, then continue to Output 5 and Output 6.
Tell the user:

> The thumbnail generation failed. The brief is saved at
> `outputs/thumbnail-brief.md`. You can run the generation manually with
> the command above once the issue is resolved, or use any image generation
> tool with the brief as your prompt.

Do not stop the skill because of a thumbnail generation failure.

---

### Output 5: Pinned comment

**Research rules (all must apply):**
- Pinned comments are indexed by YouTube. Include the primary keyword
  naturally in the text.
- Pose one open-ended question that viewers genuinely want to answer.
  Opinion prompts ("What do you think of X?") generate approximately 30% more
  replies than neutral prompts ("Let me know if you have questions").
- 1-3 sentences only. One micro-CTA at the end (e.g. "Drop your answer below"
  or "I read every reply").
- Do not repeat the title. Share one fact or observation that is NOT in the
  video, or that extends the video's conversation.
- Tone: match the foundation's voice adjectives. First-person, warm.

Write to `outputs/pinned-comment.txt`.

---

### Output 6: Community post

**Research rules (all must apply):**
- This is the launch-day post in a three-touch cadence (tease 1-2 days
  before, launch day, recap 3-7 days after). Write for launch day.
- 1-2 sentences hook. Lead with a statement that creates a knowledge gap or
  makes a claim that needs resolving. Then one optional question.
- Text posts under 150 characters get the most full reads. Aim for under
  150 characters for the hook, then a brief second sentence if needed.
- Do not simply announce "new video is up". That is noise. The post must give
  a reason to click beyond "it exists".
- Tone: match the foundation. First-person.

Write to `outputs/community-post.txt`.

---

## Step 5: Write run.json

Write `outputs/run.json` capturing:

```json
{
  "channel_slug": "<slug>",
  "video_slug": "<date>-<video-slug>",
  "run_date": "<YYYY-MM-DD>",
  "foundation_path": "channels/<slug>/foundation.md",
  "inputs": {
    "title_draft": "<user's draft or null>",
    "description_draft": "<user's draft or null>",
    "topic_brief": "<user's brief>",
    "character_reference": "<path or null>",
    "video_screenshots": ["<paths>"],
    "competitor_thumbnails": ["<paths or null>"]
  },
  "outputs": {
    "title": "outputs/title.txt",
    "title_alternatives": "outputs/title-alternatives.md",
    "description": "outputs/description.md",
    "thumbnail_brief": "outputs/thumbnail-brief.md",
    "thumbnail_image": "outputs/thumbnail.png",
    "pinned_comment": "outputs/pinned-comment.txt",
    "community_post": "outputs/community-post.txt"
  },
  "thumbnail_generation_succeeded": true
}
```

Set `thumbnail_generation_succeeded` to `false` if the gpt-image-2 call
failed.

---

## Step 6: Confirm completion

List every file written with its path. Then say:

> Suggested next steps:
>
> 1. Review the title alternatives in `outputs/title-alternatives.md` and
>    pick the strongest one for your audience and context.
> 2. Copy the description from `outputs/description.md` into YouTube Studio.
>    If you want chapter markers, reply here with your timecodes and I'll
>    add them.
> 3. Check the thumbnail at `outputs/thumbnail.png`. If it needs adjusting,
>    edit the brief in `outputs/thumbnail-brief.md` and re-run the generation
>    command.
> 4. Pin the comment in `outputs/pinned-comment.txt` immediately after
>    publishing. Replying to early comments in the first 60 minutes boosts
>    early engagement signals.
> 5. Post the community post in `outputs/community-post.txt` at publish time.

---

## Embedded behaviours (enforced throughout)

These rules apply to every output this skill produces. They are not optional.

**Foundation first.** Read the foundation before generating any output. Every
output must be consistent with the foundation's voice adjectives, locale,
banned phrases, must-include phrases, colour palette, and hard rules.

**No em-dashes.** Not in titles, descriptions, comments, or community posts.
Use a full stop, comma, colon, or parentheses.

**Thumbnail text never copies the title.** Redundancy wastes both assets.
The thumbnail earns the click; the title provides additional context.

**Locale consistency.** If the foundation specifies British English, use it
throughout. All outputs must be internally consistent in spelling (colour not
color, optimise not optimize, whilst not while).

**Title alternatives must use different formulas.** Number-based, curiosity-
gap, how-to, and story-hook are the four base formulas. Each alternative must
use a different one. Three variants of one idea are not three alternatives.

**No clickbait.** A curiosity gap is valid only if the video closes it.
Gaps that the video does not close lift CTR for 24 hours then trigger
suppression as average view duration drops.

**gpt-image-2 prompt: one paragraph, no variants.** Synthesise the thumbnail
brief into one focused paragraph. Do not produce multiple prompt options or
parenthetical alternatives within the prompt. The brief already contains the
decisions; the prompt executes them.
