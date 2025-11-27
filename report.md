
# Report

## Step 1 - Spend 30 mins listening to Cartesia

### 1.1. Specify how you did this?

#### 1.1.1. Initial Investigation (Ready)

 - My first step was to sign up for an account and open the playground (play.cartesia.ai) to "learn by doing" and 
 - After trying a few different voices and expression settings in the Playground GUI, I skimmed the documentation (https://docs.cartesia.ai/build-with-cartesia/sonic-3/)
 - My primary goal when reading the documentation and playing with the Playground was to identify the different 'levers' that were available to change *how* the speach was generated.
 - From the docs, two things stood out to me specifically: 1) The first was that although Sonic 3 responded / adapted to punctuation, it did not respond directly to other text 'formatting' like italics and capitalization (both of which are commonly used in formal and informal writing to denote a change in tone); and 2) I noted that some voices were "more expressive" than others.
 - I tried to use these more expressive voices in my testing to ensure I was getting the best and latest version of the model.

 #### 1.1.2. Enabling more robust testing

 - After playing around on the Playground and identifing some specific areas of improvement for the model (see Step 2.1 below for details), I wanted to be able to more easily compare the results of Cartesia with ElevenLabs side-by-side without having to worry about copying and pasting.
 - I asked Claude Code to spin up a lightweight Streamlit app that I could use to generate TTS from both APIs from the same input prompt, similar to the 'Chatbot Arena' but for speech. 
 - Throughout this exercise I made a few updates to the app using GPT-5 through Codex (e.g. the ability to add an API key, the 'Generation Time' tracker).
 - I have used Streamlit for many personal and work projects in the past and I find it a great way to focus on getting a very simple and usable GUI layer on top of the core logic / idea that you are working on - perfect for this use case. 
 - I primarily used this locally, but I pushed it to the Streamlit community cloud if you want to give it a try (you may need to add your own API key) - https://chrism202-cartesia-exploration-and-assessment-app-claude-d3yoiy.streamlit.app/
 - Please note that this app is 90% vibe coded, so I make no claims to the quality of the code :) 


### 1.2. What were you listening for specifically?
 - Go beyond simple "did it work"
 - Does it sound human and normal for normal, basic text generation use cases ... yes
 - I did not experience any significant uncanny valley, and anything I did experience I would say was probably more because I was listening intentionally for it
 - My hypothesis is that if I recieved a phonecall and this voice was on the other end, I would not suspect it was AI based on the voice

 - From my experience on Alexa, I know that the way that humans and models generate speech is extremely nuanced and tiny tweaks on the modeling side can lead to significant apparent changes in the customer experience.
 - The primary thing I wanted to test was how much the expressiveness could be influenced without losing any of the nuance of how real humans speak. 

 - There is a fantastic comedy sketch from a few years ago where these incredible actors debate how specifically to do the famous "to be or not to be" speech from Hamlet - https://www.youtube.com/watch?v=RJXiep-yGBw
 - This video shows how the emphasis of one word or part of a phrase can change the whole meaning of it. 

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

## Step 2 - Specify 2-3 Aspects in which the model can improve

### 2.1. Areas of Improvement

2. Specify 2-3 aspects in which you think the model can improve. For each aspect, come up with an example of a transcript, and have a recorded output of that transcript. Specify whether the area of improvement is consistent (happens in every case) or probabilistic (happens in some cases).


 - Language / pronounciation
 - More difference between emotion


#### Things to Try
P0;
 - Long form news bulliten
 - 


#### Areas that were fine



#### Areas that needed improvement / weren't great
 - Dialects and spelling variants (Aluminium)


#### Areas that were bad
 - Multilingual / code-switching




1. Pronunciation of rare / OOV words
What to test: Long, unusual words, technical jargon, low-frequency vocabulary.
	•	“The otorhinolaryngologist recommended a rhinopharyngolaryngoscopy."
	•	“He studied deoxyribonucleic acid in the cryoelectron microscope lab.”

2. Proper names (people, places, brands)
What to test: Uncommon names, non-English names, ambiguous names, brand names.
	•	“Nguyễn met Siobhán at the café on Rue de la Boétie.”
	•	“We switched from Huawei to Xiaomi before flying through Changi.”

3. Homographs & heteronyms (context-dependent pronunciation)
What to test: Words spelled the same but pronounced differently depending on meaning.
	•	“I have to record a new record every week.”
	•	“They desert their post in the desert.”
	•	“She will present the present to the class.”

4. Prosody, rhythm, and phrasing
What to test: Natural pausing, grouping of phrases, sentence melody.
	•	Sentences with complex nesting:
“The proposal, which, despite numerous critiques from the committee, she submitted anyway, was ultimately approved.”
	•	Sentences where pause changes meaning:
“Let’s eat, grandma.” vs. “Let’s eat grandma.”

5. Emphasis and contrastive stress
What to test: Does it place emphasis on the right word given context?
	•	“I didn’t say he stole the money.” (7 different meanings depending on which word is stressed.)
	•	“She said she might come, not that she would.”
You can’t easily auto-check this, but human listeners hear it immediately.

6. Punctuation and sentence boundaries
What to test: Intonation around commas, colons, quotes, and parentheses.
	•	“He said, ‘I’m not sure,’ and then he left.”
	•	“This is, in my opinion, a terrible idea.”
	•	“She bought three things: apples, which she loves; oranges, which she hates; and bananas.”

7. Numbers, dates, times, currencies
What to test: How text normalization is handled.
	•	“The budget increased from $1,234 to $12,340.50 between 2015 and 2025.”
	•	“She ran 5k in 19:45, averaging 6:21 per mile.”
	•	“Call me at 03/04/05 at 06:07.” (Ambiguous date formats.)
	•	“The temperature dropped from 32°F to 0°C overnight.”

8. Acronyms, abbreviations, and symbols
What to test: When to spell out vs. read as a word.
	•	“NASA worked with the U.S. DoD and the UK’s NHS.”
	•	“The file is saved as config.yaml in the etc directory.”
	•	“He got a Ph.D. from MIT and now works at OpenAI, Inc.”
	 - Also try things like “vs.”, “e.g.”, “i.e.”, emoticons, etc.

9. Multilingual & code-switching text
What to test: Language switching and foreign phrases.
	•	“He said, ‘C’est la vie,’ and walked away.”
	•	“Our meeting is mañana, so bring the final dossier.”
	•	“The talk was titled ‘机器学习 in Modern Healthcare’.”

10. Dialects and spelling variants
What to test: American vs British spelling and pronunciation; regional vocabulary.
	•	“The aluminium foil was in the boot of the car.”
	•	“She lives in an apartment, but calls it a flat.”
	•	“The schedule was posted in the laboratory.”

11. Emotion & expressive range (if supported)
What to test: Can it sound sad, excited, sarcastic, etc. without going uncanny?
Include explicit emotional context in text:
	•	“She whispered, barely holding back tears, ‘I think I’ve lost everything.’”
	•	“He shouted, ‘Yes! We did it!’ over the roar of the crowd.”
	•	“She replied, ‘Oh, great, another meeting,’ with obvious sarcasm.”

12. Long-form consistency and coherence
What to test: Voice stability, speaking rate, and prosody over long passages.
	•	3–5 minute news article with varied sentence lengths.
	•	A chapter of a book with dialogue, description, and exposition.

13. Dialogue with multiple speakers
What to test: Turn-taking, quote handling, and optional speaker distinction.
	•	“ ‘Are you coming?’ she asked. ‘I’m not sure,’ he replied. ‘It depends on the weather,’ she said.”
	•	Rapid alternation between short lines of dialogue.

14. Disfluencies and casual speech
What to test: Naturalness with filler words, false starts, interjections.
	•	“Well, um, I mean, it’s not that bad, you know?”
	•	“So, yeah, I was going to, uh, tell you about the thing, but then I forgot.”
	•	“Hmm… okay, let me think.”

15. Lists, enumerations, and structures
What to test: Prosody across list items; clarity of structure.
	•	“There are three reasons: first, the cost; second, the timeline; and third, the risk.”
	•	Bulleted-style text:
“One, gather requirements. Two, design the system. Three, implement and test. Four, deploy.”.

16. Very short vs. very long sentences
What to test: Handling extremes of length.
	•	Short: “Stop.” “No.” “Seriously?”
	•	Overlong: a 60–80 word sentence with several subordinate clauses.

17. Capitalization, emojis, and “noisy” text
What to test: Robustness to modern, messy input.
	•	“I’m SO excited right now!!! 😂😂😂”
	•	“gonna be late lol brb in 5”
	•	“IMPORTANT: DO NOT PRESS THE RED BUTTON.”

18. Whispering, shouting, and speaking rate (if controllable)
What to test: Stability when you push style/controls to extremes.
	•	Same sentence synthesized at slow, normal, and very fast rates.
	•	If the model has style tags like <whisper> / <shout>, combine them with tricky text:
“ Don’t tell anyone, but the safe code is 4937. ”

19. Background noise robustness (for input text from ASR, if relevant)
What to test: How TTS copes with transcripts that have ASR errors or tags.
	•	ASR-style text: “I’m [INAUDIBLE] sure but I think it’s fine.”
	•	Mis-capitalized or unpunctuated text from real ASR.

20. Speaker identity (for multi-voice or voice-cloning models)
What to test: Does the voice stay consistent across different content types?
	•	Same speaker reading:
	•	Casual conversation
	•	Technical documentation
	•	Emotional monologue
	•	Compare timbre, accent, and speaking rate between samples.
 20+12





### 2.2. Bonus Comparison

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




## Step 4 - A gift from the modeling team

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
