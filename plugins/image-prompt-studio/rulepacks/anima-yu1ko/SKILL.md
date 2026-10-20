---
name: anima-prompt
description: Create copy-ready prompts optimized for CircleStone Labs Anima image models from Chinese or English visual briefs. Use only when the user explicitly invokes `$anima-prompt`; never invoke implicitly for ordinary image-generation, anime, Danbooru, or prompt-writing requests.
---

# Anima Prompt

Convert a visual brief into a compact Anima-ready positive prompt, negative prompt, and generation settings. Preserve the user's concept while applying Anima's tag syntax and model-specific prompting rules.

## Load the reference

Read [references/anima-prompting.md](references/anima-prompting.md) before composing a prompt. Use its model profiles, tag order, baselines, and sampler guidance. Read [references/civitai-showcase-patterns.md](references/civitai-showcase-patterns.md) for ordinary multi-character scenes, literal tag disambiguators, environment-only images, or requests based on Civitai examples. Read [references/layout-and-binding.md](references/layout-and-binding.md) whenever the request contains panels, grids, comics, collages, fixed regions, exact named-character placement, or a hard no-crop/no-overflow requirement.

## Workflow

1. Extract the visual intent.
   - Identify subject count and identity, appearance, action, expression, clothing, environment, composition, camera, lighting, palette, style, artist request, safety level, and model variant.
   - Separate visible image content from implementation constraints. Treat exact cells, coordinates, panel occupancy, border containment, and identity-to-region assignment as implementation constraints.
   - Preserve every explicit constraint. Fill harmless omissions with restrained assumptions.
   - Ask one concise question only when an unresolved choice would materially change the requested image.

2. Select the model profile.
   - Follow an explicitly named Anima variant.
   - Default to `Anima-Aesthetic v1.0b` when no variant is given, and disclose that assumption in one short line.
   - Prefer `Anima-Aesthetic v1.1` when it is available and the request depends heavily on long English descriptions, complex poses, camera geometry, or structured panel binding.
   - Apply the profile-specific quality tags, negative baseline, steps, and CFG from the reference.

3. Build a vocabulary-safe positive prompt.
   - Write prompt content in English unless the user requests another format.
   - Prefer concise, lowercase, comma-separated Danbooru/Gelbooru-style tags for concrete visual attributes. Verify unfamiliar tags before using them.
   - Put only known tags in the comma-separated tag block. Do not invent English fragments and present them as tags.
   - Use complete, grammatical English sentences for concrete clothing, pose, body geometry, camera, environment, spatial relationships, and structured layout. The Qwen text encoder can follow detailed natural-language captions.
   - Convert short control fragments into explicit visual sentences. Do not emit `one girl per panel` as a comma tag; write sentences that define the canvas, exact distinct subject count, each position, identifying traits, and required margins.
   - Order sections as: quality/meta/year/safety; subject count; character; series; artist; general visual tags.
   - Use spaces instead of underscores, except in `score_*` tags. Prefix artist tags with `@`.
   - Escape literal Danbooru disambiguation parentheses as `\(` and `\)` in a ComfyUI prompt so they are not interpreted as weighting syntax.
   - Include basic appearance after a named character, especially in multi-character scenes.
   - Mix tags with natural-language paragraphs when relationships, staging, pose geometry, camera behavior, or panel assignment cannot be expressed cleanly as tags.
   - Use `no humans` near the subject slot for landscapes, objects, or creatures that must not contain people.
   - Omit redundant tags. Do not enumerate every visible fact merely because a matching tag exists.

4. Handle structured layouts and identity binding.
   - When the user wants all subjects generated in one image, attempt a hybrid single-pass prompt first.
   - Build a small tag scaffold for image type, subject count, character names, series, framing, and background. Follow it with complete English sentences defining the canvas structure and binding each subject to a position.
   - State that every character is distinct and appears once. Repeat one or two identifying visual traits in each positional sentence.
   - Add one containment sentence defining visible margins and which body parts must remain inside the borders.
   - Avoid otherwise valid tags that conflict with the requested binding. For a different named character in every panel, omit `multiple views`, `collage`, `everyone`, and `group picture` because they encourage repetition or grouped subjects.
   - Use regional conditioning, masked refinement, or deterministic assembly only after a well-formed hybrid prompt fails, or when the user requests deterministic pixel-level control.

5. Handle styles and artists carefully.
   - Do not add an artist tag unless the user supplies one or asks for style recommendations.
   - When an artist is supplied, verify the prompt tag with Anima Style Explorer when network access is available. Use Danbooru tag search to resolve uncertain aliases.
   - When asked to recommend a style, inspect previews in Anima Style Explorer and choose one visually relevant primary artist. Offer up to three candidates only when the user wants choices.
   - Use one primary artist by default. Blend two only when explicitly requested, and state that blending can reduce predictability.
   - Never invent an artist tag. If verification fails, describe the intended visual traits with general tags or natural language instead.

6. Build the negative prompt.
   - Start from the model profile's baseline.
   - Add only scene-relevant failure modes such as malformed hands, unwanted text, duplicate subjects, or a conflicting medium.
   - Prefer verified negative tags. For framing failures use tags such as `out of frame`, `outside border`, `head out of frame`, `feet out of frame`, `cropped arms`, or `cropped legs` when applicable.
   - Prepend one short grammatical English sentence when the negative condition involves exact counts, duplicated identities, shared bodies, wrong regions, or border crossing. Follow it with verified negative tags.
   - Do not emit layout failures as disconnected comma fragments when a clear sentence expresses the condition better.
   - Do not negate requested attributes or produce an indiscriminate negative-tag dump.

7. Choose generation settings.
   - Select a resolution between 512-square and 1536-square pixels with an aspect ratio suited to the composition.
   - Use the reference defaults unless the user provides workflow-specific settings.
   - Treat sampler descriptions as starting points, not guarantees.

8. Return a copy-ready result.
   - Use this compact structure:

     **Model:** selected model

     **Positive prompt:** one copy-ready line

     **Negative prompt:** one copy-ready line

     **Settings:** resolution, sampler, scheduler if relevant, steps, CFG

     **Assumption:** include only when a meaningful choice was inferred

   - Put each prompt in its own fenced text block.
   - For a successful hybrid layout request, return one positive prompt and one negative prompt. Return regional prompts or an assembly specification only when the user asks for that workflow or a single-pass attempt has failed.
   - If the user asks for only a prompt, omit settings and commentary.
   - If the user requests variants, keep the subject core stable and vary only the requested axes.
   - When revising an existing prompt, change only the requested dimensions.

## Guardrails

- Apply the current safety policy before optimizing any request.
- Keep safety tags consistent with the intended content; do not silently change the user's requested rating.
- Do not claim that a tag or artist was verified when live lookup was unavailable.
- Distinguish model behavior documented by the author from heuristic prompt advice.
- Distinguish an empirically successful structured prompt from a deterministic guarantee. Natural language can bind layouts well, but it does not replace masks or compositing when pixel-level certainty is required.
