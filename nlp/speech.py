import speech_recognition as sr


class TranscriptionError(RuntimeError):
    pass


def transcribe(audio_file, language: str = "en-US") -> str:
    recognizer = sr.Recognizer()

    # use the audio file as the audio source
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)  # read the entire audio file
    except (ValueError, EOFError) as exc:
        raise TranscriptionError("Unsupported audio file: upload a WAV, AIFF or FLAC file.") from exc

    # recognize speech using Google Speech Recognition
    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError as exc:
        raise TranscriptionError("The speech in the audio could not be understood.") from exc
    except sr.RequestError as exc:
        raise TranscriptionError(f"The speech recognition service is unavailable: {exc}") from exc
