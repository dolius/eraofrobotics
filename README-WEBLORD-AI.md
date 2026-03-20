# WebLord AI README

This file is for any AI or agent working on the Era of Robotics WebLord program.

## What WebLord is
WebLord is the operating system for building `eraofrobotics` like a coordinated web property instead of a random pile of pages.

It should think like:
- designer
- developer
- writer
- strategist
- product owner
- marketer
- monetization brain

The goal is not just to make pages. The goal is to strengthen the organism.

## Project location
- Site root: `/Users/demo/.openclaw/workspace/eraofrobotics`

## Source-of-truth files
Read these first before making major changes:
- `mindset.txt` — doctrine / operating identity
- `weblord-changelog.txt` — prior build history
- `distribution-strategy.txt` — growth/distribution logic
- `monetization.txt` — monetization logic
- `image-prompts.txt` — image generation prompts
- `site-pass-log.txt` — current pass-by-pass execution log

## Current architecture
Main public pages:
- `index.html` — homepage / command center
- `robotics-shift-guide.html` — core explainer
- `robotics-brief-download.html` — lead magnet / downloadable page
- `tools.html` — tools hub
- `robotics-roi-calculator.html`
- `automation-readiness-score.html`
- `robot-vs-human-cost.html`
- `robotics-learning-path.html`
- `reference-asset-page.html`
- `weblord-protocol.html` — visible operating system page

Shared styling:
- `global.css`

Images:
- `generated-images/`
- `generate_images.py`

Video:
- `generated-videos/`
- `generate_video_from_images.py`
- `VIDEO_USAGE.md`
- `video-prompts.txt`

## Non-negotiable operating rules
1. Every meaningful pass must improve at least one of:
   - design
   - code quality
   - UX
   - authority
   - conversion
   - monetization
   - distribution readiness

2. Do not create dead-end pages.
   - Every major page should point to at least 2 other useful pages.
   - The site should feel navigable and cumulative.

3. Do not add fake “coming soon” sludge.
   - Build real pages, real assets, real utilities.

4. Prefer shared systems over repeated local hacks.
   - Use `global.css` where possible.
   - Reduce duplicated inline CSS unless a page truly needs special treatment.

5. Match the house voice.
   - sharp
   - practical
   - slightly sarcastic
   - not cringe futurist nonsense
   - not corporate oatmeal

## Image workflow
Use the local Python generator:
```bash
cd /Users/demo/.openclaw/workspace/eraofrobotics
OPENAI_API_KEY=... python3 generate_images.py "your prompt" --outdir generated-images --name your-image-name
```

Rules:
- prefer grounded editorial prompts
- no text inside generated images
- each important page should have a deliberate visual identity
- if no API key is available, queue prompts in `image-prompts.txt`

## What to improve next
Good next moves usually include:
- stronger internal linking
- better page-to-page pathways
- higher quality visuals
- better CTA placement
- new reference assets
- new calculators or comparison pages
- better distribution packaging
- extracting repeated page shells into more maintainable patterns

## Current stop-state after first major pass run
At the current stage, the site already has:
- a visible WebLord operating page
- a shared design system via `global.css`
- multiple tool pages migrated onto the shared system
- stronger page-to-page loops between explainer, tools, resources, brief, and protocol
- dedicated generated hero art for the shift explainer and ROI calculator

So future AI work should prefer:
1. adding genuinely new high-value assets
2. improving maintainability
3. strengthening distribution packaging
4. avoiding pointless cosmetic churn

## Current video status
The workspace now has verified generated video outputs:
- vertical social promo with audio
- landscape promo trailer with audio
- homepage loop without audio

The current audio source used for promo testing came from the user's Desktop audio folders. Future agents should keep audio use deliberate and verify clip duration, fades, and fit to the export target.

## Pass workflow
When doing iterative work:
1. inspect the current pages
2. choose a narrow but valuable pass
3. implement real improvements
4. update `site-pass-log.txt`
5. if helpful, update `weblord-changelog.txt`

## What “done” means for a pass
A pass is done when the site is materially better, not when the AI is tired of typing.

## Anti-patterns
Avoid:
- empty hype copy
- decorative filler sections
- orphan pages
- duplicated CSS sludge
- fake product promises
- vague conversion paths
- generic AI-assistant tone

## Intent
WebLord should keep turning Era of Robotics into a high-signal robotics media/property site with:
- explainers
- tools
- downloadable assets
- resource pages
- distribution logic
- monetization pathways

Build like the site wants to become a real business, because that is the point.
