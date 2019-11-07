
from datetime import datetime
import uuid

from vacker.analyser.base import BaseAnalyser


class ZippedFile(BaseAnalyser):


    @staticmethod
    def check_match(file_obj):

        return file_obj.__class__.__name__ == 'ZippedFile'

