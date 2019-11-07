
from datetime import datetime

from vacker.analyser.base import BaseAnalyser


class TarredFile(BaseAnalyser):


    @staticmethod
    def check_match(file_obj):

        return file_obj.__class__.__name__ == 'TarredFile'

