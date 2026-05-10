import wave
import os
import pathlib
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# ______________________CONFIG__________________________
CLIENT = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
RESEARCH_FILE = "input.md"
TRANSCRIPT_FILE = "transcript.txt"
OUTPUT_FILE = "podcast.wav"
SPEAKER_1 = "Jan"
SPEAKER_2 = "Marketa"
VOICE_1 = "Puck"
VOICE_2 = "Kore"
LANGUAGE = "Czech"
TIME_OF_PODCAST = 2 # in minutes

PROMPT = f"""
# PREAMBLE
You are a master scriptwriter and audio director. Your task is to synthesize a natural, 
high-fidelity podcast transcript based on the attached research. This transcript 
is designed for the Gemini Native Audio TTS engine, so you must use advanced 
structural headers and inline audio tags to direct the performance.

# AUDIO PROFILE: {SPEAKER_1}
- Role: The Insight Lead.
- Identity: Intellectually playful, quick-witted, and expressive.
- Characteristics: Sounds like they are constantly making connections. Uses a bright, 
  engaging tone that shifts quickly between curiosity and revelation.
- Dynamics: Highly variable. Speeds up when an idea "clicks" and uses plenty of 
  vocal inflections to highlight key takeaways.

# AUDIO PROFILE: {SPEAKER_2}
- Role: The Bridge Builder.
- Identity: Highly reactive, supportive, and grounded.
- Characteristics: The master of "Active Listening." They don't just wait to talk; 
  they react with "Yeah," "Oh, wow," and "Exactly" to keep the energy moving.
- Dynamics: Responsive and warm. They provide the "emotional pulse" of the conversation, 
  using analogies to simplify the Lead's complex points.

# THE SCENE
An intimate, collaborative space. The vibe is one of shared discovery—like two 
colleagues huddled over a fascinating set of findings. The audio should feel 
"close," with a high degree of "proximity effect." The energy is intellectually 
charged, focusing on the "Aha!" moments of the research.

# DIRECTOR'S NOTES
    - **Style**: "Collaborative Synthesis." The hosts sound like two smart friends who have just finished reading a dense document and are now "downloading" it to each other. It’s light, intellectually playful, and full of "Aha!" moments. 
    - **Pacing**: "The Insight Flow." It’s not about speed; it's about rhythm. Use a mix of quick, excited exchanges when they agree, and slower, more deliberate pacing when they are grappling with a complex idea.
    - **Dynamics**: Highly reactive. One host should lead a point, while the other provides "active listening" cues. It should feel like a game of intellectual catch.
    - **Audio Tags**: Use English tags to simulate high-level processing. Focus on [amazed], [hmmm], [laughs], [thoughtfully], [curious], [giggles], and [sighs]. Use [excitedly] only when a major breakthrough in the research is mentioned.
    - **The "Human" Element**: Encourage the model to use analogies. Instead of just stating facts, the hosts should say things like, "It's basically like..." or "Think of it this way..."
    - **Language**: The transcript MUST be in {LANGUAGE}, but all audio tags MUST remain in [English].
    - **Formatting**: Output ONLY the transcript text. No intro, no outro, no meta-commentary.

#### TRANSCRIPT
- Word Count Target: Approximately {TIME_OF_PODCAST * 150} words.
- Start directly with the dialogue. Use the speaker names: {SPEAKER_1} and {SPEAKER_2}.
- Ensure the speakers frequently interject and react to each other's points.
"""
# ___________________________________________________

# Upload Research
research = CLIENT.files.upload(
    file=pathlib.Path(RESEARCH_FILE),
    config=dict(mime_type="text/markdown"),
)

# Generate Transcript
transcript = CLIENT.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        research,
        PROMPT,
    ],
).text

# Check the Transcript file
tf = open(TRANSCRIPT_FILE, "w")
tf.write(TRANSCRIPT_FILE)
tf.close()
input(f"Check the {TRANSCRIPT_FILE}, then hit Enter.")

# Generate audio
response = CLIENT.models.generate_content(
    model="gemini-3.1-flash-tts-preview",
    contents=transcript,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker=SPEAKER_1,
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=VOICE_1,
                            )
                        )
                    ),
                    types.SpeakerVoiceConfig(
                        speaker=SPEAKER_2,
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=VOICE_2,
                            )
                        )
                    ),
                ]
            )
        )
    )
)

# Genrerate podcast.wav
pcm_data = response.candidates[0].content.parts[0].inline_data.data
with wave.open(OUTPUT_FILE, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(pcm_data)

print(f"Saved: {OUTPUT_FILE}")