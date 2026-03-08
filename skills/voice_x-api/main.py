def ingest_audio(file_path, msg_id, metadata=None):
    transcript = "[placeholder] x-api транскрипция из {}".format(file_path)
    summary = summarize(transcript)
    return transcript, summary


def summarize(text):
    return text


def store_result(msg_id, transcript, summary, meta=None):
    return {'msg_id': msg_id, 'transcript': transcript, 'summary': summary, 'meta': meta or {}}
