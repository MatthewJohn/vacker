
from datetime import datetime

from vacker.analyser.base import BaseAnalyser


class TarredFile(BaseAnalyser):


    @staticmethod
    def check_match(file_obj):

        return file_obj.__class__.__name__ == 'TarredFile'

    @classmethod
    def get_file_properties(cls, file_obj):
        file_obj.properties['g_size'] = int(file_obj.tar_object.size)
