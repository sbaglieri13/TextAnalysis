import speech_recognition as sr


def run(audio_file):
    # use the audio file as the audio source
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)  # read the entire audio file

    # recognize speech using Sphinx
    try:
        text = recognizer.recognize_sphinx(audio)
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

