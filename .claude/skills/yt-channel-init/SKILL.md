---
name: yt-channel-init
description: >
  One-time channel foundation interview. Builds channels/<slug>/foundation.md,
  which every other yt-studio skill reads as context. Run once per channel;
  re-run any time to update specific sections.
when-to-use: >
  Before you run yt-video-optimise for the first time on a new channel, or
  when the channel's niche, audience, or visual identity has shifted
  significantly and the foundation file needs a refresh.
tools:
  - Read
  - Write
  - Edit
---

# Skill body

## Overview for Claude Code

This skill conducts a structured interview with the user, then writes a
`channels/<slug>/foundation.md` that captures everything about the channel:
identity, niche, audience, voice, visual style, competition, goals, and hard
rules. Every subsequent optimisation skill reads this file, so accuracy here
directly affects output quality across all future runs.

Work through the eight sections below **one at a time**. After each section,
wait for the user's complete reply before moving to the next. Do not batch
questions across sections.

---

## Step 1: Greet and orient

Say the following (adapt naturally, keep the substance):

> Welcome to the YouTube Channel Studio setup. This interview takes about
> 15-20 minutes. I'll ask you eight short sections of questions, one at a
> time, and then write a foundation file that tells me everything I need to
> know about your channel before I help with individual videos. You can update
> it any time by re-running this skill.

Then ask:

> What is your channel handle? (e.g. `@SilverForgeStudio`)

Derive the slug: strip the `@`, lowercase everything, replace spaces and
special characters with hyphens. Example: `@SilverForgeStudio` becomes
`silverforgestudio`. Store this as `<slug>`.

Check whether `channels/<slug>/foundation.md` already exists using the Read
tool. If it does, say:

> I found an existing foundation file for this channel. Do you want to update
> specific sections, or start the full interview again from scratch?

If the user wants to update specific sections only, skip to those sections and
leave the others unchanged. If starting fresh, continue with Section 1.

---

## Section 1: Identity

Ask these questions together (they are a single coherent block):

> Let's start with the basics.
>
> 1. What is the full channel name as it appears on YouTube?
> 2. What is the channel URL? (e.g. youtube.com/@SilverForgeStudio)
> 3. What is the channel's current public description (the About section on
>    the channel page)? Paste it if you have it, or say "none yet".
> 4. What year did you start the channel, or plan to launch it?
> 5. What is your name, and are you on camera, off camera, or both?

If the user is unsure about their public description, suggest:

> That's fine. We can draft one after the foundation is complete, or you can
> leave it blank for now and I'll flag it as a gap to fill.

---

## Section 2: Niche and positioning

> Now let's pin down what this channel is actually about.
>
> 1. What is the broad vertical? (e.g. jewellery making, AI for business,
>    fitness, cooking, personal finance)
> 2. What is the sub-niche? Be specific. (e.g. "hand-fabricated gold
>    jewellery" rather than "jewellery")
> 3. What is your unique angle versus other channels in this space? What do
>    you do or say that they do not?
> 4. What will this channel NOT cover? Naming what you exclude is as important
>    as what you include.

If the user struggles with the unique angle, offer this prompt:

> Think about it this way: if someone watched your channel and then watched
> three others in your niche, what one thing would they say only you offer?
> It could be a technique, a perspective, a context, or a tone.

---

## Section 3: Audience

> Tell me about the person who watches this channel.
>
> 1. Describe your primary viewer: rough age range, context (professional,
>    hobbyist, student), and what brings them here.
> 2. What problem or frustration do they arrive with?
> 3. What aspiration do they have when they watch your content?
> 4. Why would they watch YOUR channel specifically, rather than another
>    channel in the same niche?

Push for specificity. If the user writes something vague like "anyone
interested in jewellery making", follow up:

> Let's sharpen that. A specific persona will make every title, thumbnail, and
> description more effective. For example: "independent jewellers aged 30-50
> who trained traditionally and are now curious about whether CAD tools will
> replace their craft" is a persona. "Everyone interested in jewellery" is
> not. Can we narrow it down?

---

## Section 4: Voice and tone

> How does this channel sound and feel?
>
> 1. Give me 3-5 adjectives that describe the channel's voice. Here are three
>    clusters to anchor your thinking:
>
>    - "warm, educational, no-jargon" (approachable teacher)
>    - "cinematic, sparse, premium" (aesthetic-first, minimal narration)
>    - "fast-paced, direct, practical" (no fluff, get to the point fast)
>
>    Your voice might mix elements, or sit outside all three. That is fine.
>
> 2. Language locale: British English, American English, or other?
> 3. How formal is the language? (e.g. "I reckon" vs "In my view" vs
>    "Research suggests")
> 4. Any phrases that must NEVER appear? (e.g. em-dashes, "as an AI", filler
>    words, specific clichés)
> 5. Any phrases that must always appear or that are signature to your brand?
>    (e.g. a sign-off, a recurring term, your studio name)

---

## Section 5: Visual identity

> Let's talk about how the channel looks.
>
> 1. What is the visual mood? (e.g. cinematic, raw and handheld, editorial,
>    warm studio, high-key clean white, dark and atmospheric)
> 2. What are 2-5 brand colours? Hex values if you have them; named colours
>    (e.g. "deep navy, warm gold, cream") if not.
> 3. Any brand fonts?
> 4. Any recurring visual motifs? (e.g. a specific texture, material, setting,
>    or object that appears in most thumbnails)
> 5. If you appear on camera: how do you typically present in thumbnails?
>    (Expression style, framing, clothing colour, any visual signature)
> 6. Is there a character reference image I can use as the visual anchor for
>    thumbnail generation? If yes, what is the file path?

If the user has no reference image yet, note in the foundation:
`thumbnail_reference_image: none_yet` and add a note that the optimise skill
will ask for one per video.

---

## Section 6: Competition and inspiration

> I want to understand your landscape.
>
> 1. List 5 competitor or peer channels, with URLs. For each, tell me one
>    thing they do well that you admire (even if you would not copy it).
> 2. List up to 3 channels you do NOT want to copy, and briefly why. (What
>    would be a wrong turn for your brand?)

Capture the URLs precisely. They will be used for future competitor research
runs.

If the user can only name 3 competitors, that is acceptable. Do not block
progress. Note the gap.

---

## Section 7: Goals and cadence

> What are you building toward?
>
> 1. Subscriber target and timeline. (e.g. "10k by December 2026")
> 2. Watch-time or revenue target, if any.
> 3. Monetisation strategy: AdSense, brand deals, course sales, community,
>    physical product, or a combination?
> 4. Posting cadence: how many videos per week or month?
> 5. Content pillars: 3-5 recurring themes or formats that cover the channel.
>    (e.g. "tutorials", "behind-the-scenes process", "material deep-dives",
>    "Q+A", "product reviews")

If the user is unsure about cadence, suggest:

> A common starting pattern for a new channel is one video per week for the
> first six months, then review. Consistency matters more than frequency in
> the early stage. What is the most you can sustain without burning out?

---

## Section 8: Hard rules

> Finally, the guardrails.
>
> 1. Any hashtags that must appear on every video?
> 2. How do you end your videos? (End screen pattern, verbal CTA, or both)
> 3. What is your standard call-to-action? (e.g. "subscribe", "comment
>    below", "join the community", "book a session")
> 4. Anything that must never appear on this channel? (Specific topics,
>    phrases, visual styles, competitor names, etc.)
> 5. Any accessibility commitments? (e.g. always add captions, always include
>    audio description, always provide a transcript)

---

## Optional: Examples that already worked

After Section 8, ask:

> One optional step. If you already have videos on this channel, paste up to
> 3 titles and their descriptions that performed well for you. This gives me a
> baseline to learn from. Skip this if the channel is brand new or if you are
> not sure what "performed well" means yet.

If the user provides examples, store them verbatim in the foundation under
`## What already worked`.

---

## Validation before writing

Before writing the file, confirm these four fields are present. If any are
missing, ask for them before proceeding:

- `niche` (sub-niche level, not just broad vertical)
- `audience_persona` (specific enough to describe one person, not a category)
- `tone_adjectives` (at least 3)
- `posting_cadence` (at minimum a frequency, e.g. "1 per week")

If any field is absent, say:

> Before I write the foundation, I need one more answer. [Ask the specific
> missing question.]

---

## Write the foundation file

Write `channels/<slug>/foundation.md` using the Write tool.

The file must follow this structure exactly (heading names must match):

```
# Channel Foundation: <Channel Name>

Handle: @<handle>
URL: <url>
Slug: <slug>
Founded: <year>
Creator: <name>, <on-camera / off-camera / both>
Last updated: <YYYY-MM-DD>

## Identity

[Channel name, handle, public description, founding context]

## Niche and Positioning

[Vertical, sub-niche, unique angle, what the channel does NOT cover]

## Audience

[Primary persona: demographic + psychographic, pain, aspiration, reason they
choose THIS channel]

## Voice and Tone

Adjectives: [list]
Locale: [British / American / other]
Formality: [description]
Banned phrases: [list or "none specified"]
Must-include phrases: [list or "none specified"]

## Visual Identity

Mood: [description]
Colours: [list with hex or named palette]
Fonts: [list or "not specified"]
Visual motifs: [description or "none specified"]
On-camera presenter: [description of how they appear in thumbnails]
Thumbnail reference image: [file path or "none_yet"]

## Competition and Inspiration

### Channels to learn from
[List with URL + one-sentence note per channel]

### Channels NOT to copy
[List with one-sentence reason per channel]

## Goals and Cadence

Subscriber target: [target + timeline]
Watch-time / revenue target: [or "not specified"]
Monetisation: [strategy]
Posting cadence: [frequency]
Content pillars: [list]

## Hard Rules

Default hashtags: [list or "none specified"]
End-screen pattern: [description]
Standard CTA: [description]
Never appear: [list or "none specified"]
Accessibility: [commitments or "standard captions recommended"]

## What Already Worked

[Paste the user's provided examples verbatim, or "No examples provided."]

## Strategic Positioning Summary

[Write a 3-4 sentence paragraph that synthesises the whole channel. Cover:
what the channel is, who it is for, what makes it different, and what success
looks like. This paragraph is read first by the optimise skill before any
per-video work.]
```

The Strategic Positioning Summary is the only section you write in your own
words. Everything else is the user's answers, lightly edited for clarity.

---

## Confirm completion

After writing the file, tell the user:

> Foundation written to `channels/<slug>/foundation.md`.

Then give a one-paragraph summary of what the channel is, who it serves, and
what the strategic differentiation is (draw from the Strategic Positioning
Summary you just wrote).

Then say:

> You can update any section at any time by re-running this skill and choosing
> "update specific sections". Next step: run `yt-video-optimise` when you
> have a video ready to publish.
