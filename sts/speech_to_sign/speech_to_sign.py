import glob
import os
from sts.speech_to_sign.audio_recording import RecordingThread
from sts.speech_to_sign.speech_to_text import SpeechToText
from sts.speech_to_sign.animate import Animate


class SpeechToSign:
    def __init__(self, show_speed=5):
        # to start recording
        self.__rth = RecordingThread()
        self.__stt = SpeechToText()
        self.__animator = Animate('')
        self.__animator.set_speed(show_speed)
        self.__sentence_queue = []
        self.__loop = True

    def start_pipeline(self):
        """Runs the complete pipeline of audio conversion to lemmatized text

        Output:
            list: A list of strings representing the lemmatized text
        """

        while self.__loop:
            try:
                file_name = glob.glob("output*")
                if len(file_name) != 0:
                    # Converting a single recorded audio file into text
                    text = self.__stt.convert_recorded_audio(file_name[0])
                    lemmatized_text = self.__stt.lemmatize(text)
                    # print(lemmatized_text)
                    sentence = ' '.join(lemmatized_text)
                    print(f'spoken:({sentence})')
                    if sentence != '':
                        self.__sentence_queue.append(sentence)
                        self.sentence_listener()

                    os.remove(file_name[0])
                # else:
                #     continue
            except ValueError:
                continue
            except TypeError:
                continue

    def sentence_listener(self):
        """


        Returns:
            None

        """
        while len(self.__sentence_queue) > 0:
            self.__animator.show_sign(self.__sentence_queue[0])
            del self.__sentence_queue[0]

    def stop_pipline(self):
        self.__rth.stop()
        self.__loop = False