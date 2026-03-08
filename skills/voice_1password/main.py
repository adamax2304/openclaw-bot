def ingest_audio(file_path, msg_id, metadata=None):
    # Minimal placeholder: pretend we transcribed the audio
    transcript = "[placeholder] транскрипция аудио из {}".format(file_path)
    summary = "[placeholder] краткое резюме" 
    return transcript, summary


def summarize(text):
    return text[:200] + ("..." if len(text) > 200 else "")


def store_result(msg_id, transcript, summary, meta=None):
    # Placeholder: do nothing
    return {
        'msg_id': msg_id,
        'transcript': transcript,
        'summary': summary,
        'meta': meta or {}
    }
