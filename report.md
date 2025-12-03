
# Report

Chris Morrison's report for the Model Behavior Product Manager take-home.

## Step 1 - Spend 30 mins listening to Cartesia

### 1.1. Specify how you did this?

#### 1.1.1. Initial Investigation (Ready)

 - My first step was to sign up for an account and open the playground (play.cartesia.ai) to "learn by doing". 
 - After trying a few different voices and expression settings in the Playground GUI, I skimmed the documentation (https://docs.cartesia.ai/build-with-cartesia/sonic-3/)
 - My primary goal when reading the documentation and playing with the Playground was to identify the different 'levers' that were available to change *how* the speach was generated.
 - From the docs, two things stood out to me specifically: 1) The first was that although Sonic 3 responded / adapted to punctuation, it did not respond directly to other text 'formatting' like italics and capitalization (both of which are commonly used in formal and informal writing to denote a change in tone); and 2) I noted that some voices were "more expressive" than others.
 - I tried to use these more expressive voices in my testing to ensure I was getting the best and latest version of the model.

 #### 1.1.2. Enabling more robust testing (Ready)

 - After playing around on the Playground and identifing some specific areas of improvement for the model (see Step 2.1 below for details), I wanted to be able to more easily compare the results of Cartesia with ElevenLabs side-by-side without having to worry about copying and pasting.
 - I asked Claude Code to spin up a lightweight Streamlit app that I could use to generate TTS from both APIs from the same input prompt, similar to the popular 'LM/Chatbot Arena' but for speech. 
 - I have used Streamlit for many personal and work projects in the past and I find it a great way to focus on getting a very simple and usable GUI layer on top of the core logic of a project that you are working on - perfect for this use case. 
 - I primarily used this locally, but I pushed it to the Streamlit community cloud if you want to give it a try (you may need to add your own API key) - https://chrism202-cartesia-exploration-and-assessment-app-claude-d3yoiy.streamlit.app/
 - Throughout this exercise I made a few updates to the app using GPT-5 through Codex (e.g. the ability to add an API key, the 'Generation Time' tracker).


### 1.2. What were you listening for specifically? (Ready)
 - From my experience on Alexa, I know that the way that humans and models generate speech is extremely nuanced and tiny tweaks on the modeling side can lead to significant changes in the customer experience.
 - The first thing I was listening for was a simple 'does it work' ... does it sound like a normal person for 99.9% of the speech.
 - This is quite a high bar because even one unnatural expression can ruin the whole experience.
 - In this regard I am happy to say that Cartesia was excellent right out of the box, without any additional prompting or tweaking to punctuation, it was able to generate an excellently 'expressed' TTS ([Example](supporting_files/highly_expressive_cartesia_output_example.mp3)). 
 - In comparison, key competitors like ElevenLabs generate a very 'flat' sounding audio ouput from the same prompt ([Example](supporting_files/flat_sounding_elevenlabs_output_example.mp3))
 
 - Beyond basic functionality, the most important thing I wanted to test was how much the expressiveness could be influenced without losing any of the nuance of how real humans speak. 
 - To assess this, I refer to an excellent comedy sketch I saw a few years ago, where some incredible stage actors debate how specifically to do the famous "to be or not to be" speech from Hamlet - https://www.youtube.com/watch?v=RJXiep-yGBw.
 - This video shows how the emphasis of one word or part of a phrase can change the whole meaning of the same phrase. Specifically, it shows how small and nuanced those changes should be.

 - My initial goal when experimenting with the Cartesia TTS model was to emulate this sketch by assessing how nuanced the changes would be in the output, for a given input. 
 - I experimented with different punctuation and noted how small differences in the input resulted in nuanced changes to the models generated output ([Example 1](supporting_files/to_be1_cartesia_tts_output.mp3), [Example 2](supporting_files/to_be2_cartesia_tts_output.mp3))

 - Overall I would say that my thoughts after this initial testing is that out of the box, the Cartesia model worked excellently, with additional prompt instructions not being required (only optional).
 - However I did note that I wasn't able to use some common ways to add emphasis like bolding, italics, and capitalization - adding this 'formatting' type input didn't result in a different output, as might be expected (since this is a common way to emphasize tone/expression in written text).

## Step 2 - Specify 2-3 Aspects in which the model can improve

2. Specify 2-3 aspects in which you think the model can improve. For each aspect, come up with an example of a transcript, and have a recorded output of that transcript. Specify whether the area of improvement is consistent (happens in every case) or probabilistic (happens in some cases).

### 2.1. Areas of Improvement

 - After testing of different speech dimensions, I identified two areas to focus on analyzing for model improvement: Locale-specific pronunciation; and Acronyms, numbers & symbols.
 - I selected these two areas because they represent fundamental capabilities that will scale across all use cases of the model, and aren't edge case functionality - it is critical that the model gets these things right.

#### Pronounciation (Locale-specific and code-switching) + Bonus comparison
 - Being able to pronounce words correctly within the locale / dialect context is critical for natual human-like TTS. 
 - This is a nuanced area because some words are pronounced differently depending on the dialect.
 - For example in for example in US english, "croissant" (French loanword) is typically pronounced to rhyme with 'want', whereas in British English it would be pronounced more like the French version (although native French speakers would debate the similarity!).
 - Other loanwords are typically pronounced using the native pronounciation, even if the word itself would be pronounced differently if written in English.
 - A classic illustrative example of this is Mexican-Spanish placenames like Guadalajara and Tiajuana which are pronounced with a Spanish 'hwa' in place of the hard 'j/g', even by English speakers with no Spanish language skills.
 - The below table outlines a handful of examples illustrating how the Cartesia model performs on these tricky situations, and how a competitor model (ElevenLabs) performs on the same prompt.


| Sub-dimension                     | Example Transcript                                      | Improvement Required (Cartesia)                                                                              | Issue Consistency? | Competitor Rating | Competitor Assessment                                                                                                      | Cartesia Recording                                                                     | Competitor Recording                                                                | Comment                                                             |
| --------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------ | ----------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Loanwords #1                      | Geneviève will visit Guadalajara en route to São Paulo. | None of the words were pronounced correctly                                                                  | Consistent         | Need to meet      | "Geneviève", "en" and "São Paulo" are pronounced poorly, but Guadalajara is spot-on for a natural American pronounciation. | [Link](supporting_files/locale_cartesia_output.mp3)                                    | [Link](supporting_files/locale_elevenlabs_output.mp3.mp3)                           | Tested using standard US voices                                     |
| Loanwords #2                      | Nguyễn met Siobhán at the café on Rue de la Boétie.     | None of the words were pronounced correctly                                                                  | Consistent         | Need to meet      | "Nguyen" and "Siobhan" misspronounced, but French words were pronounced well (potentially \*too\* well)                    | [Link](supporting_files/cartesia_loanwords_cafe.mp3)                                   | [Link](supporting_files/elevenlabs_loanwords_cafe.mp3)                              | Tested using standard US voices                                     |
| Locale-specific pronounciation #1 | The schedule was posted in the laboratory.              | Laboratory is not quite pronounced correctly, sounds too 'American' for a British pronounciation             | Consistent         | Need to meet      | Both are pronounced accurately for a Brit                                                                                  | [Link](supporting_files/locale_specific_pronounciation_cartesia_output_charlotte.mp3)  | [Link](supporting_files/locale_specific_pronounciation_elevenlabs_output_lily.mp3)  | Tested using UK voice (Charlotte for Cartesia, Lily for ElevenLabs) |
| Locale-specific pronounciation #2 | The aluminium foil was in the boot of the car.          | Aluminum is pronounced halfway between American pronounciation and British pronounciation.                   | Consistent         | Need to meet      | Pronounced accurately for a Brit                                                                                           | [Link](supporting_files/locale_specific2_pronounciation_cartesia_output_charlotte.mp3) | [Link](supporting_files/locale_specific2_pronounciation_elevenlabs_output_lily.mp3) | Tested using UK voice (Charlotte for Cartesia, Lily for ElevenLabs) |
| Locale-specific loanwords         | Flavored croissants are very niche                      | Croissants and niche are pronounced strangely for a Brittish accent (niche doesn't rhyme enough with leash). | Consistent         | Need to meet      | As a Brit, the pronounciation of both croissants and niche are spot on.                                                    | [Link](supporting_files/cartesia_locale-specific_loanwords_charlotte_uk.mp3)           | [Link](supporting_files/elevenlabs_locale-specific_loanwords_lily_uk.mp3)           | Tested using UK voice (Charlotte for Cartesia, Lily for ElevenLabs) |





#### Acronyms, Symbols & Numbers + Bonus comparison (Ready)
 - Being able to accurately and naturally articulate Acronyms, Symbols and Numbers is a critical skill for a TTS model to have, since these situations show up in almost every single real-world use case imaginable (legal, financial, support calls, etc).
 - A failure on this task (which human readers/speakers would find trivial) won't just result in an "uncanny valley" situation, it can fundamentally cause confusion or mislead the end user, breaking all trust that might have been earned.
 - Being able to do this task accurately demonstrates that the model has a deeper understanding and contextual awareness of the information being communicated.

 
| Sub-dimension | Example Transcript                                     | Improvement Required (Cartesia)                                                                                                                                       | Issue Consistency? | Competitor Rating     | Competitor Assessment                                                  | Cartesia Recording                                     | Competitor Recording                                     | Comment                         |
| ------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | --------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------- | ------------------------------- |
| Filenames     | The file is saved as config.yaml in the etc directory. | Voice trails off and sounds hessitant, strange pronounciation of "[…]aml" and "etc"                                                                                   | Consistent         | Cartesia > Competitor | Performs worse on both filename and etc pronounciation                 | [Link](supporting_files/filenames_cartesia_output.mp3) | [Link](supporting_files/filenames_elevenlabs_output.mp3) | Tested using standard US voices |
| Acronyms      | He got a Ph.D. from MIT and now works at OpenAI, Inc.  | Mostly correct except that PHD is pronounced P-H-dot-D.                                                                                                               | Consistent         | Cartesia < Competitor | Performs better, natururally sounding out the PHD without punctuation. | [Link](supporting_files/phd_cartesia_output.mp3)       | [Link](supporting_files/phd_elevenlabs_output.mp3)       | Tested using standard US voices |
| Numbers      | Call me at 03/04/05 at 06:07.                          | Doesn't correctly identify the date format so says "April fifth" instead of "Fourth of March 2005" or "Third of April 2005" (either are correct depending on context) | Consistent         | Cartesia > Competitor | Performs poorly, simply reads out the numbers.                         | [Link](supporting_files/date_cartesia_output.mp3)      | [Link](supporting_files/date_elevenlabs_output.mp3)      | Tested using standard US voices |







## Step 3 - Pick one of the aspects to dive deeper on

Choice: Pronounciation (Locale-specific and code-switching)

### Why did you choose that one?

 - This is important because 20% of households speak another language
 - They will immediately pick up if the word is pronounced incorrectly


### How would you operationalize data collection & evaluations?

#### Priority 1: Golden Set Comparison

 - Ultimately the only way to get a strong signal for improvements in this area is to generate a golden set of roughly 100-1,000 words or phrases (per language/locale) that represent words that have challenging or novel pronunciation (either because they are loanwords or for another reason).
 - At every major model release, this golden set would be used to assess the performance of the new model, by generating a fresh TTS for each of the golden set words and phrases. 
 - This TTS (generated by the new model) would then have to be manually annotated, ideally by native speakers, along specific dimensions like accent and  pronunciation.
 - This annotation process would involve humans listening to the generated TTS and comparing it against a known-good recording of a native speaker speaking the same words/phrases, and rating the generated TTS when compared to the known-good recording along the relevant dimensions.
 - For this specific area, native speakers are critical to success, since non-native speakers would miss a lot of the nuance that makes this evaluation important and valuable.
 - These generated TTS would then be annotated by native speakers (must be native, non-native speakers would miss a lot of the nuance that makes this exercise critical).
 
 #### Priority 2: Introducing Automation

 - Because this process is time-consuming and expensive (native speakers for some countries will have very high hourly rates and be hard to come by), it is  likely that this process could only be performed once or twice for each major model release.
 - This is a problem, because as the modeling team are working to improve the model, they need a short feedback loop to validate if their experiments / new approaches are working. 
 - If the model team wants to know if a new approach is valid, they cannot wait months to get the information they need to make an informed decision. 
 - For this reason it is important to supplement this golden set assessment with an automated process that might not be perfect but can be run ad-hoc, to  quickly and cheaply provide a directional signal for ongoing experiments and novel modeling approaches.
 - This specific task is a challenging one to solve in an automated way, but setting up a simple ASR/STT (Automatic Speech Recognition/Speech to Text) pipeline using a phoneme-based ASR (e.g. wav2vec2phoneme) could enable a rapid comparison of pronunciation at a semi-granular level.
 - This pipeline would work by creating a known-good IPA (International Phonetic Alphabet) representation of the previously described golden set of challenging words and phrases, which would then act as the baseline to compare against ASR-generated phonemes which were fed the generated TTS from the latest model.
 - This setup would enable reasonably fine-grained identification of localized pronunciation, for example for UK voices, `/ˈkwæsɒ̃/` would be the IPA groundtruth label for "croissant", whereas for a US voice, it would be `/kɹəˈsɑnt/`.
 - This approach would enable the modeling and product team to rapidly assess the performance improvements of the model as needed, but would come with a couple of tradeoffs.
 - One tradeoff is that this approach is a discrete representation of a continuous variable, so small differences in the pronunciation would result in less granular changes in the IPA representation. 
 - This means that small changes in how the model pronounces words could result in large changes to the measurement of this rapid benchmark.
 - Another tradeoff is that this approach would effectively introduce an additional variable, namely, the ASR model, that might impact the results of the 
 - In other words, if the ASR model had specific limitations in language or pronunciation, that could lead to incorrect or misleading results.
 - However, over time, through comparison with manually generated known-good labels, the correlation of this rapid offline benchmark against the manual measurement could be dialed in, and more confidence could be placed in the numbers over time.


## Step 4 - A gift from the modeling team

A Gift from Modeling Team
The model team found a way to give the model a “context”. A context is a 512-bit vector that is passed into the API calls. It encodes the entire context for the model to nail current TTS generation, and outputs a new context that includes the context and everything that has been generated. Alternatively, the model can receive context and any text and just “add to context”, without generating speech from this.

For example:
addToContext(C,“The next sentence should be said very loudly, as if you are very angry”)
C = generate(C,“This is unacceptable!”)

You can think about the context as representing roughly a voice actor’s state-of-mind when speaking out their part in a conversation, or doing a longer narration. It doesn’t guide the model on *what to say*, but *how* to say it.



### Step 4.1. What are 2-3 usages of this context feature that you could see? What is the first one you would try?

 - This functionality effectively enables a deeper level of customization for the model output, but without having to re-train the model (which takes time and GPUs).
 - For example if we wanted to add a new accent, e.g. Geordie (from Newcastle in the UK), we could encode the pronunciation information in the context vector that could enable an accurate Geordie accent without having to generate and collect training data and re-train the model (a Geordie sounding model would have limited appeal...).
 - Below are three possible use cases for this context feature, in priority order - Cross-language performance matching would be the first use case I would investigate.

#### Priority 1: Cross-language performance matching in dubbing

 - Use `context` vector to carry the acting choices from the original performance into a localized/dubbed version.
 - This capability has applications wherever audio and video require localization (YouTube, Podcasts, Instagram/Tik Tok, etc).
 - This would involve extracting the context vector representation of the original voice vocal arc throughout the duration of the recording, and re-inserting it during the generation of the localized dub.
 - This is extremely useful, and would result in a higher quality automatically generated dub, where the outputted audio mirrors the original in tone, emotional shape, phrasing changes, etc.






#### Priority 2: Listener-personalized context blending / Explicit voice preference

 - Explicit voice preference for voice assistants like Alexa and Siri - if I tell them to speak louder or faster, then I can easily load that up with each new interaction. 
 - Over time this would make the _way_ that these assistants speak personalized, in addition to the things that they do / say.
 - This approach would use a per-listener preference context to blend with content context at synthesis time (e.g., “serious news” and “slightly faster, less dramatic”).
 - We could build the preference vector from behavior signals (skips/replays/ratings, "can you repeat that") or explicit requests (“a bit louder").
 - In addition to voice assistants, this approach has applicability in personalization at scale for podcasts and news apps (e.g. The Economist AI generated narration).
 - For the customer, the voice delivery feels personalized and tailored to their needs without adjusting sliders or updating profiles.


#### Priority 3: Single, dedicated support agent
- Create the perception of a single, dedicated support agent for call-center tasks, that has context of how the conversation has gone previously.
 - This agent would be the equivalent of interacting with a small business with excellent customer service - when you call up, you know who will answer and they can immediately recall who you are and the prior conversations that you have had (and adopt the appropriate tone as a result).
 - Using a context vector is much better than trying to store the state outside the model and then trying to fake it or replicate it using voice tags.


### Step 4.2. Write the launch blog post for this feature.





