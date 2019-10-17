
from datetime import datetime
import zipfile

from vacker.analyser.base import BaseAnalyser
from vacker.analyser.factory import Factory
from vacker.analyser.file import ZippedFile


class ZipAnalyser(BaseAnalyser):


    @staticmethod
    def check_match(file_obj):
        return file_obj.mime_type == 'application/zip'

    @classmethod
    def get_file_properties(cls, file_obj):
        try:
            with zipfile.ZipFile(file_obj.path) as myzip:

                for i in myzip.infolist():
                    if not i.is_dir():
                        zf = ZippedFile(myzip, i)
                        Factory().analyse_file(zf)
                        file_obj.additional_file(zf)

        except Exception as exc:
            print(exc)
