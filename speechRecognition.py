import speech_recognition as sr


# Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition API. The
# Google Speech Recognition API key is specified by key. If not specified, it uses a generic key that works out of
# the box. This should generally be used for personal or testing purposes only, as it may be revoked by Google at any
# time.
def run():
    # create a speech recognition object
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        # obtain audio from the microphone
        print("Say something!")
        recognizer.pause_threshold = 0.7
        audio_data = recognizer.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = recognizer.recognize_google(audio_data)

        return text

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))