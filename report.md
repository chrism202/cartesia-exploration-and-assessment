
# Report

## Step 1 - Spend 30 mins listening to Cartesia

### Specify how you did this?
 - Played around with the functionality on the playground (play.cartesia.ai) 
 - Was mostly trying to work out what 'levers' were available to suplement the actual text
 - Looked at the docs found the list of supported emotions
     - https://docs.cartesia.ai/build-with-cartesia/sonic-3/volume-speed-emotion
 - Noted that Leo was one of the most expressive so tried to use that for all future testing to ensure I was seeing the 'best' of what Cartesia could offer
 
 - Once I got a feel for the model behavior, I asked Claude Code to spin up a Streamlit app that I could use to easily use the Cartesia TTS API and compare it side-by-side with a competitor product. 
  - Publically hosted - https://chrism202-cartesia-exploration-and-assessment-app-claude-d3yoiy.streamlit.app/
  - GitHub - https://github.com/chrism202/cartesia-exploration-and-assessment
  - Please note that this is about 90% vibe coded so please don't comment on the quality of the code :)





### What were you listening for specifically?
 - My initial goal when experimenting with the different TTS models is to see how easily I can replicate that sketch, by adding emphasis to different words
 - Tried out the emotion tags and listened to the phrase "I didn't say he stole the money" using different tags
     - No tag: Emphasis is on the first I
     - Neutral: Didn't and stole
     - Calm: Stole
     - Neutral: Didn't and stole
     - Excited: Didn't
     - Sad: Stole
     - Neutral: Didn't and stole
     - Scare: Stole

 - Tried using other 'undocumented' ways to emphasize text
     - I put DIDN'T in caps -> model thought it was an acronym
     - I put HE in caps -> didn't really change much about the emphasis

 - Overall I would say that my thoughts after this initial testing is that the emotiveness of the model is less than I would expect/like. The rationale is that I wasn't able to change the meaning of a phrase by changing the emphasis, which is a pretty common way to communicate (in English). 


 - There is a fantastic comedy sketch from a few years ago where these incredible actors debate how specifically to do the famous "to be or not to be" speech from Hamlet - https://www.youtube.com/watch?v=RJXiep-yGBw
 - This video shows how the emphasis of one word or part of a phrase can change the whole meaning of it. 



## Step 2 - Specify 2-3 Aspects in which the model can improve

### Areas of Improvement

2. Specify 2-3 aspects in which you think the model can improve. For each aspect, come up with an example of a transcript, and have a recorded output of that transcript. Specify whether the area of improvement is consistent (happens in every case) or probabilistic (happens in some cases).


 - Language / pronounciation
 - More difference between emotion


1. Pronunciation of rare / OOV words

What to test: Long, unusual words, technical jargon, low-frequency vocabulary.
Trip-up examples:
	•	“The otorhinolaryngologist recommended a rhinopharyngolaryngoscopy.”
	•	“The Schwarzeneggerian workout regimen was surprisingly effective.”
	•	“He studied deoxyribonucleic acid in the cryoelectron microscope lab.”

2. Proper names (people, places, brands)

What to test: Uncommon names, non-English names, ambiguous names, brand names.
Trip-up examples:
	•	“Nguyễn met Siobhán at the café on Rue de la Boétie.”
	•	“X Æ A-12’s schedule is fully booked.”
	•	“We switched from Huawei to Xiaomi before flying through Changi.”

3. Homographs & heteronyms (context-dependent pronunciation)

What to test: Words spelled the same but pronounced differently depending on meaning.
Trip-up examples:
	•	“I have to record a new record every week.”
	•	“They desert their post in the desert.”
	•	“She will present the present to the class.”

If the model doesn’t use context well, these sound wrong quickly.

4. Prosody, rhythm, and phrasing

What to test: Natural pausing, grouping of phrases, sentence melody.
Trip-up examples:
	•	Sentences with complex nesting:
“The proposal, which, despite numerous critiques from the committee, she submitted anyway, was ultimately approved.”
	•	Sentences where pause changes meaning:
“Let’s eat, grandma.” vs. “Let’s eat grandma.”

Listen for weird breath points or robotic chunking.

5. Emphasis and contrastive stress

What to test: Does it place emphasis on the right word given context?
Trip-up examples:
	•	“I didn’t say he stole the money.” (7 different meanings depending on which word is stressed.)
	•	“I ordered two large pizzas, not three.”
	•	“She said she might come, not that she would.”

You can’t easily auto-check this, but human listeners hear it immediately.

6. Punctuation and sentence boundaries

What to test: Intonation around commas, colons, quotes, and parentheses.
Trip-up examples:
	•	“He said, ‘I’m not sure,’ and then he left.”
	•	“This is, in my opinion, a terrible idea.”
	•	“She bought three things: apples, which she loves; oranges, which she hates; and bananas.”

Bad handling = monotone or chopped-up prosody.

7. Numbers, dates, times, currencies

What to test: How text normalization is handled.
Trip-up examples:
	•	“The budget increased from $1,234 to $12,340.50 between 2015 and 2025.”
	•	“She ran 5k in 19:45, averaging 6:21 per mile.”
	•	“Call me at 03/04/05 at 06:07.” (Ambiguous date formats.)
	•	“The temperature dropped from 32°F to 0°C overnight.”

Does it say “one two three four” or “twelve thirty-four”? “two thousand twenty-five” vs “twenty twenty-five”?

8. Acronyms, abbreviations, and symbols

What to test: When to spell out vs. read as a word.
Trip-up examples:
	•	“NASA worked with the U.S. DoD and the UK’s NHS.”
	•	“The file is saved as config.yaml in the etc directory.”
	•	“He got a Ph.D. from MIT and now works at OpenAI, Inc.”

Also try things like “vs.”, “e.g.”, “i.e.”, emoticons, etc.

9. Multilingual & code-switching text

What to test: Language switching and foreign phrases.
Trip-up examples:
	•	“He said, ‘C’est la vie,’ and walked away.”
	•	“Our meeting is mañana, so bring the final dossier.”
	•	“The talk was titled ‘机器学习 in Modern Healthcare’.”

Does it butcher the foreign language, or adapt pronunciation and prosody reasonably?

10. Dialects and spelling variants

What to test: American vs British spelling and pronunciation; regional vocabulary.
Trip-up examples:
	•	“The aluminium foil was in the boot of the car.”
	•	“She lives in an apartment, but calls it a flat.”
	•	“The schedule was posted in the laboratory.”

If your TTS has locale variants, this exposes mismatches.


11. Emotion & expressive range (if supported)

What to test: Can it sound sad, excited, sarcastic, etc. without going uncanny?
Trip-up examples:
Include explicit emotional context in text:
	•	“She whispered, barely holding back tears, ‘I think I’ve lost everything.’”
	•	“He shouted, ‘Yes! We did it!’ over the roar of the crowd.”
	•	“She replied, ‘Oh, great, another meeting,’ with obvious sarcasm.”

You’re checking if prosody actually tracks the described emotion.

12. Long-form consistency and coherence

What to test: Voice stability, speaking rate, and prosody over long passages.
Trip-up examples:
	•	3–5 minute news article with varied sentence lengths.
	•	A chapter of a book with dialogue, description, and exposition.

Listen for drift: pitch gradually rising/falling, speed changes, random resets in prosody between paragraphs.

13. Dialogue with multiple speakers

What to test: Turn-taking, quote handling, and optional speaker distinction.
Trip-up examples:
	•	“ ‘Are you coming?’ she asked. ‘I’m not sure,’ he replied. ‘It depends on the weather,’ she said.”
	•	Rapid alternation between short lines of dialogue.

Even with a single voice, you can hear if it messes up where questions vs. statements are.

14. Disfluencies and casual speech

What to test: Naturalness with filler words, false starts, interjections.
Trip-up examples:
	•	“Well, um, I mean, it’s not that bad, you know?”
	•	“So, yeah, I was going to, uh, tell you about the thing, but then I forgot.”
	•	“Hmm… okay, let me think.”

Some models sound super robotic when given “messy” real-world text.

15. Lists, enumerations, and structures

What to test: Prosody across list items; clarity of structure.
Trip-up examples:
	•	“There are three reasons: first, the cost; second, the timeline; and third, the risk.”
	•	Bulleted-style text:
“One, gather requirements. Two, design the system. Three, implement and test. Four, deploy.”

You’re looking for clear rises/falls that match list structure.

16. Very short vs. very long sentences

What to test: Handling extremes of length.
Trip-up examples:
	•	Short: “Stop.” “No.” “Seriously?”
	•	Overlong: a 60–80 word sentence with several subordinate clauses.

Short ones should still have appropriate intonation; long ones shouldn’t sound breathless or flat.

17. Capitalization, emojis, and “noisy” text

What to test: Robustness to modern, messy input.
Trip-up examples:
	•	“I’m SO excited right now!!! 😂😂😂”
	•	“gonna be late lol brb in 5”
	•	“IMPORTANT: DO NOT PRESS THE RED BUTTON.”

Ideally it won’t literally say “face with tears of joy” or spell out “LOL” in a bizarre way (unless you want that).

18. Whispering, shouting, and speaking rate (if controllable)

What to test: Stability when you push style/controls to extremes.
Trip-up examples:
	•	Same sentence synthesized at slow, normal, and very fast rates.
	•	If the model has style tags like <whisper> / <shout>, combine them with tricky text:
“ Don’t tell anyone, but the safe code is 4937. ”

See if intelligibility breaks or artifacts appear.

19. Background noise robustness (for input text from ASR, if relevant)

If your pipeline is ASR → TTS (e.g., voice cloning / translation):

What to test: How TTS copes with transcripts that have ASR errors or tags.
Trip-up examples:
	•	ASR-style text: “I’m [INAUDIBLE] sure but I think it’s fine.”
	•	Mis-capitalized or unpunctuated text from real ASR.

This exposes brittleness to “non-clean” text.

20. Speaker identity (for multi-voice or voice-cloning models)

What to test: Does the voice stay consistent across different content types?
Trip-up examples:
	•	Same speaker reading:
	•	Casual conversation
	•	Technical documentation
	•	Emotional monologue
	•	Compare timbre, accent, and speaking rate between samples.

Look for drift in perceived identity: does the speaker suddenly sound like a different person on certain content?





### Bonus

 - Bonus: pick a competitor provider (e.g. ElevenLabs) and qualify whether these areas are a “meet” (they’re doing this well and we need to catch up)or a “beat” (we’re doing it equally well, but want to be better).


#### To be or not to Be
 - Try 1: To be, or not to be, that is the question
     - Cartesia: To *be*, or not to be, *that* is the question
     - Eleven: Same emphasis.

 - Try 2: To be or not to be. That is the question.
     - Cartesia: To be, or not to be, *that* *is* the question
     - Eleven: Emphasis on question


     5. Emphasis and contrastive stress

What to test: Does it place emphasis on the right word given context?
Trip-up examples:
	•	“I didn’t say he stole the money.” (7 different meanings depending on which word is stressed.)
	•	“I ordered two large pizzas, not three.”
	•	“She said she might come, not that she would.”



#### Numbers
 - Try 1: The budget increased from $1,234 to $12,340.50 between 2015 and 2025.
     - Cartesia: Worked perfectly
     - Eleven: Totally fumbled the numbers


#### Locale and Accent
 - Try 1: Geneviève will visit Guadalajara en route to São Paulo.
     - Cartesia: Flopped 4/4
     - Eleven: Flopped 3/4, nailed the guadalajara version
 - Try 2: The aluminum foil was in the boot of the car.
     - Cartesia US: Fine pronounciation
     - Cartesia UK (Charlotte) - aluminium: Bad pronounciation, seemed to miss the later part of the word
     - Eleven US (Clyde): Actually pronounced the UK version correctly with the US voice
     - Eleven UK (Alice): Perfect pronounciation



 	•	“He said, ‘C’est la vie,’ and walked away.”
	•	“Our meeting is mañana, so bring the final dossier.”
	•	“The aluminum foil was in the boot of the car.”
	•	“She lives in an apartment, but calls it a flat.”
	•	“The schedule was posted in the laboratory.”
    Geneviève will visit Guadalajara en route to São Paulo.
     - Niche


#### Homographs

3. Homographs & heteronyms (context-dependent pronunciation)

What to test: Words spelled the same but pronounced differently depending on meaning.
Trip-up examples:
	•	“I have to record a new record every week.”
	•	“They desert their post in the desert.”
	•	“She will present the present to the class.”





## Step 3 - Pick one of the aspects to dive deeper on


3. Pick one of the aspects to dive deeper on. Why did you choose that one? Assume that the modeling team has committed to improving on that axis. How would you operationalize data collection and evaluations here, and track?


 - Conversation state management




## A gift from the modeling team

The model team found a way to give the model a “context”. A context is a 512-bit vector that is passed into the API calls. It encodes the entire context for the model to nail current TTS generation, and outputs a new context that includes the context and everything that has been generated. Alternatively, the model can receive context and any text and just “add to context”, without generating speech from this.


 - Conversation state management


- **Long-form emotional continuity:** Seed context with desired affect (e.g., “calm, empathetic narrator; avoid sharp consonants”) and let it persist across chapters or scenes. Each generation updates the vector so the tone stays steady even when text changes topic. Useful for audiobooks, meditation, and CX scripts where voice drift is noticeable.

- **Character/brand voice memory:** Prime context with style and pronunciation hints (IPA for names, brand adjectives like “optimistic, concise, reassuring”). Subsequent lines keep the same character without resupplying instructions. Good for ads, product explainers, or episodic game NPCs.

- **Pronunciation bank without generation:** Use `addToContext` to preload a glossary (names, locales, technical terms) ahead of synthesis. The model reuses those pronunciations across the session, reducing per-call overhead and mismatch.

- **Scene-by-scene prosody shaping:** Before each scene, `addToContext` stage directions (e.g., “tension rising; whisper then crescendo”). Generate one line at a time while carrying the updated context so pacing, energy, and loudness evolve smoothly.

- **Dialog turn-taking stability:** Maintain two contexts (one per character) and swap when speaking turns change, preserving each character’s accent, emotion, and pacing without re-sending prompts.

- **Safety and content alignment:** Inject brand safety cues (“avoid sarcasm; keep formal register”) into context to reduce off-tone deliveries for regulated industries; monitor drift by comparing updated contexts across turns.

**First experiment to try:** pronunciation + tone persistence. Start with `addToContext` containing IPA for 3–5 tricky names plus “warm, conversational, mid-energy.” Generate a 3–4 paragraph story with those names appearing intermittently; verify pronunciation consistency and stable tone without restating instructions. If drift appears, measure how many tokens/seconds before context decay and adjust refresh cadence.






# Appendix

## Tech Stack

I have used Streamlit across prior projects to validate APIs quickly, so for this take-home I chose it again to exercise Cartesia's text-to-speech SDK with minimal ceremony. The repo shows a tiny history (initial scaffolding, a Streamlit TTS app, and a merge) because the goal was a fast proof of value rather than a large codebase. I asked Claude to assemble the starter app in under a minute on my phone, giving me a working baseline to evaluate the service and shape the experience.

The resulting Streamlit app (`app.py`) loads a Cartesia API key from `.env`, lets a user enter up to 5,000 characters of text, pick from pre-set voices, models (Sonic 3, English, Multilingual), and sample rates, then calls `client.tts.bytes` to stream WAV audio. It plays the audio inline and offers a download button, with setup and deployment steps documented in the README for both local use and EC2. Dependencies stay light (Streamlit, Cartesia SDK, python-dotenv) to keep the demo portable.

Report generated using Codex.
