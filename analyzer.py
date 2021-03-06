import standardizer
import essentia_analyzer
import json
import sound
import os
import settings
from jinja2 import Template


class Analyzer(object):
    def __init__(self, precision):
        self.precision = precision
        self.analyzer = essentia_analyzer.EssentiaAnalyzer()

    def run(self, settings_filename):
        with open(settings_filename, 'r') as settings_file:
            sound_features = json.load(settings_file)

        sounds = []
        for sound_filename in sound_features:
            snd = sound.Sound(sound_filename)
            features = sound_features[sound_filename]

            print('Analyzing {}'.format(snd.filename))
            self.analyzer.analyze_multiple([snd], features)

            if not snd.is_silent:
                std = standardizer.Standardizer([snd])
                std.calculate_feature_statistics()
                std.add_standardized_series()
                snd.analysis['series'] = snd.analysis['series_standardized']
                del snd.analysis['series_standardized']
                std.round_to_precision(self.precision)
            sounds.append(snd)

        json_data = {snd.filename: snd.analysis['series'] for snd in sounds}

        json_data_serialized = json.dumps(json_data, separators=(',', ':'))
        template = Template('window.audioAnalysis={{ json_data }};')
        js = template.render(json_data=json_data_serialized)

        with open(os.path.join(settings.INPUT_DIRECTORY, 'audioAnalysis.js'), 'w') as outfile:
            outfile.write(js)


if __name__ == '__main__':
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--precision',
        dest='precision',
        help='Number of digits for representing a number',
        type=int,
        required=False,
        default=3,
        choices=range(1, 17)
    )
    args = arg_parser.parse_args()

    a = Analyzer(
        precision=args.precision
    )
    a.run(os.path.join(settings.INPUT_DIRECTORY, 'features.json'))
