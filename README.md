# Gemini Podcast Maker

Turns a markdown file into a two-host podcast `.wav` using Gemini similar to Notebook LM.

It does two Gemini calls:
1. Reads `input.md` and writes a transcript with two hosts.
2. Sends the transcript to the multi-speaker TTS model and writes `podcast.wav`.

## Install

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"
```

## Use

1. Put your source material in `input.md`.
2. (Optional) edit the constants at the top of `main.py`:
   - `SPEAKER_1`, `SPEAKER_2` — host names
   - `VOICE_1`, `VOICE_2` — voices from `voices.txt`
   - `LANGUAGE` — language of the script
   - `PROMPT` - maybe a little bit of editing
   - `TIME_OF_PODCAST` — target length in minutes (≈150 words/min)
3. Run:

```bash
python main.py
```

The output is written to `podcast.wav`.

## Voices

See `voices.txt` for the full list of prebuilt voices and their styles.
