from __future__ import absolute_import
from __future__ import division
import os
import settings


class Sound(object):
    def __init__(self, filename, verify_file=True):
        self.filename = filename
        self.file_path = os.path.join(settings.INPUT_DIRECTORY, self.filename)

        if verify_file:
            self.verify_file()
        
        self.analysis = {
            'series': {}
        }
        self.is_silent = False

    def verify_file(self):
        if not os.path.exists(self.file_path):
            raise Exception(
                'Could not find "{}". Make sure it exists and try again.'.format(self.file_path)
            )
