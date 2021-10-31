import json
import wave

from vosk import Model, KaldiRecognizer
from pymystem3 import Mystem


class NamesDetector:
    def __init__(self):
        self.names = set()
        self.russian = set()
        self.model = Model('vosk-model-ru-0.10')

        with open('names.txt') as file:
            self.names = set([line.strip() for line in file])
        with open('russian.txt') as file:
            self.russian = set([line.strip() for line in file])

    def _recognize_audio(self, filename):
        timestamps = []
        wf = wave.open(filename, "rb")

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            return

        rec = KaldiRecognizer(self.model, wf.getframerate())
        rec.SetWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                timestamps += result['result']

        return timestamps

    def _extract_names(self, text):
        m = Mystem()
        excluded_parts = ['CONJ', 'PR', 'PART', 'ADV']

        names = set()

        for token in m.analyze(text):
            if 'analysis' in token:
                analysis = token['analysis']
                for an in analysis:
                    lex = an['lex']
                    gr = an['gr']

                    not_excluded = all([(part not in gr) for part in excluded_parts])
                    is_in_dataset = lex in self.names and not_excluded
                    is_name_grammatically = 'gr' in an and 'имя' in gr

                    if (is_in_dataset or is_name_grammatically) and lex not in self.russian:
                        names.add(token['text'])

        return names

    def process_audio(self, filename):
        timestamps = self._recognize_audio(filename)
        names = self._extract_names(' '.join([x['word'] for x in timestamps]))
        return list(filter(lambda x: x['word'] in names, timestamps))
