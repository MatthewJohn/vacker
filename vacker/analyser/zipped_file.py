
from datetime import datetime
import uuid

from vacker.analyser.base import BaseAnalyser


class ZippedFile(BaseAnalyser):


    @staticmethod
    def check_match(file_obj):

        return file_obj.__class__.__name__ == 'ZippedFile'

    @classmethod
    def get_file_properties(cls, file_obj):
        file_obj.properties['g_size'] = int(file_obj.zip_object.file_size)
