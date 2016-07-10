from __future__ import absolute_import
from __future__ import print_function
import statistics


class Standardizer(object):
    DEVIATION_LIMIT = 4.0

    def __init__(self, sound_files):
        """
        :param sound_files: SoundFile instances with series to be analyzed and/or standardized
        :return:
        """
        self.sound_files = sound_files
        self.feature_statistics = {}

    def calculate_feature_statistics(self, series_key='series'):
        for key in self.sound_files[0].analysis[series_key]:
            self.feature_statistics[key] = {
                'min': None,
                'max': None,
                'mean': None,
                'standard_deviation': None
            }

        for feature in self.feature_statistics:
            series = []
            for sf in self.sound_files:
                series += sf.analysis[series_key][feature]

            if len(series) == 0:
                continue

            self.feature_statistics[feature]['min'] = min(series)
            self.feature_statistics[feature]['max'] = max(series)
            self.feature_statistics[feature]['mean'] = statistics.mean(series)
            self.feature_statistics[feature]['standard_deviation'] = statistics.pstdev(series)

        return self.feature_statistics

    def add_standardized_series(self):
        for sf in self.sound_files:
            if 'series_standardized' not in sf.analysis:
                sf.analysis['series_standardized'] = {}
                for feature in self.feature_statistics:
                    if isinstance(sf.analysis['series'][feature][0], list):
                        # TODO: implement standardization for features such as melbands, which are arrays within an array
                        raise Exception('Standardization for lists within a list is not implemented yet')
                    sf.analysis['series_standardized'][feature] = [
                        self.get_standardized_value(feature, value)
                        for value in sf.analysis['series'][feature]
                        ]

    def get_standardized_value(self, feature, value):
        """
        :param feature:
        :param value:
        :return: A value that makes the series have zero mean and unit variance
        """
        if self.feature_statistics[feature]['standard_deviation'] == 0.0:
            standardized_value = (value - self.feature_statistics[feature]['mean'])
        else:
            standardized_value = (value - self.feature_statistics[feature]['mean']) / \
                                 self.feature_statistics[feature]['standard_deviation']
            standardized_value = max(
                min(standardized_value, self.DEVIATION_LIMIT),
                -self.DEVIATION_LIMIT
            )  # clip extreme values
        return standardized_value
