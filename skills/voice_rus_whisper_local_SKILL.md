# voice_rus_whisper_local

- Name: voice_rus_whisper_local
- Purpose: Local speech-to-text for Telegram voice messages in Russian using Whisper, with simple extraction and local storage inside OpenClaw workspace.
- Language: Python
- Surface: ingest_audio(file_path, msg_id, metadata=None) -> transcript, summary; store_result(msg_id, transcript, summary, meta)

## Description
This skill accepts audio files (Telegram voice messages), converts input from ogg to wav, runs Whisper (local) for Russian transcription, produces a short summary, and stores results locally.

## Dependencies
- torch
- transformers (optional if using Whisper)
- whisper
- ffmpeg

## Installation
- pip install torch torchvision torchaudio
- pip install openai-whisper
- sudo apt-get install ffmpeg

## Inputs
- file_path: path to audio file (ogg, wav, mp3)
- lang: 'ru'
- msg_id: Telegram message id for storage
- metadata: optional dict with additional fields

## Outputs
- transcript: transcription text
- summary: short summary of content
- storage: saved files in workspace/voice_rus_whisper_local/

## Methods
- ingest_audio(file_path, msg_id, lang='ru', metadata=None)
  - Convert ogg to wav if needed
  - transcribe with Whisper ru model
  - generate summary (extract key phrases or first sentences)
  - return transcript, summary

- summarize(text) -> summary
- store_result(msg_id, transcript, summary, meta=None) -> path

## Example

```
transcript, summary = ingest_audio('path/to/audio.ogg', 'msg123', lang='ru')
store_result('msg123', transcript, summary, {'source':'telegram','type':'voice'})
```
