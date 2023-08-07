from pydub import AudioSegment
from google.cloud import speech


class DataExtract:
    def fetch_audio(self, file_path: str):
        """
        Fetches the audio from the file path
        :return: audio object from the file path
        """
        stereo_audio = AudioSegment.from_file(file_path)
        mono_audio = stereo_audio.set_channels(
            1
        )  # Convert to mono audio since stereo audio is not supported
        return mono_audio.raw_data

    def speech_to_text(self, audio_data: str):
        """
        Performs synchronous speech recognition on an audio file
        :param audio_data: The audio data file path.
        """
        audio_data = self.fetch_audio(file_path=audio_data)
        # Configure the speech recognition request
        config = {
            "language_code": "en-US",  # Language code for English (US)
            # Sample rate of our audio file which is set to 44.1 kHz
            "sample_rate_hertz": 44100,
            "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        }

        # Perform the transcription request
        client = speech.SpeechClient()

        audio = speech.RecognitionAudio(content=audio_data)

        resp = {"audio": audio, "config": config}

        text, confidence = "", 0

        response = client.recognize(request=resp)
        for result in response.results:
            best_alternative = result.alternatives[0]
            text = best_alternative.transcript
            confidence = round(best_alternative.confidence * 100, 2)

        return (text, confidence)


# if __name__ == "__main__":
# data_create = DataCreate()

# Fetch the audio from the file path
# data = data_create.speech_to_text(audio_data=
# "Dataset/test/1249120_1853182_11719913.wav")
# print(data)
