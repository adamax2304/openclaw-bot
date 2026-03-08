import os
import subprocess
from pathlib import Path

WORKSPACE = Path('/root/.openclaw/workspace')
STORAGE = WORKSPACE/ 'voice_rus_whisper_local'/ 'transcripts'
(SP_OK, SP_OUT) = (None, None)

def _ensure_dirs():
    STORAGE.parent.mkdir(parents=True, exist_ok=True)
    STORAGE.mkdir(parents=True, exist_ok=True)


def _ogg_to_wav(input_path: str, output_path: str) -> None:
    # use ffmpeg to convert if needed
    cmd = ['ffmpeg','-y','-i', input_path, output_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def ingest_audio(file_path: str, msg_id: str, lang: str='ru', metadata: dict=None):
    _ensure_dirs()
    input_path = Path(file_path)
    wav_path = input_path.with_suffix('.wav')
    if input_path.suffix.lower() != '.wav':
        _ogg_to_wav(str(input_path), str(wav_path))
        audio_to_use = str(wav_path)
    else:
        audio_to_use = str(input_path)

    # Whisper local via whisper.py CLI (assuming installed as 'whisper')
    # We'll call: whisper <audio> --language ru --model small (fast) or base
    model = 'small'
    cmd = ['python','-m','whisper', audio_to_use, '--language', lang, '--model', model, '--device','cpu']
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    transcript = ''
    for line in res.stdout.splitlines():
        if line.strip().startswith('Transcription'):  # simplistic
            transcript = line
    # Fallback: read last lines from stdout
    transcript = res.stdout.strip()
    summary = summarize(transcript)
    store_result(msg_id, transcript, summary, {'source':'telegram','type':'voice'})
    return transcript, summary


def summarize(text: str) -> str:
    if not text:
        return ''
    # naive summary: take first 2 sentences
    sentences = text.split('. ')
    return '. '.join(sentences[:2]).strip()


def store_result(msg_id: str, transcript: str, summary: str, meta: dict=None) -> Path:
    meta = meta or {}
    target_dir = STORAGE/ msg_id
    target_dir.mkdir(parents=True, exist_ok=True)
    t_path = target_dir/ 'transcript.txt'
    s_path = target_dir/ 'summary.txt'
    with t_path.open('w', encoding='utf-8') as f:
        f.write(transcript)
    with s_path.open('w', encoding='utf-8') as f:
        f.write(summary)
    # store meta json
    import json
    with (target_dir/ 'meta.json').open('w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return target_dir

if __name__ == '__main__':
    # quick test path (for debugging not used in production)
    print('Voice Rus Whisper Local prototype ready')
