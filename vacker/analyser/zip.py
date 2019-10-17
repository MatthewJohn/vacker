
from datetime import datetime
import zipfile

from vacker.analyser.base import BaseAnalyser
from vacker.analyser.factory import Factory
from vacker.analyser.file import ZippedFile


class ZipAnalyser(BaseAnalyser):


    @staticmethod
    def check_match(file_obj):
        print('Checkig')
        return file_obj.mime_type == 'application/zip'

    @classmethod
    def get_file_properties(cls, file_obj):
        try:
            with zipfile.ZipFile(file_obj.path) as myzip:
                print(myzip.infolist())

                for i in myzip.infolist():
                    print(i)
                    if not i.is_dir():
                        zf = ZippedFile(i, myzip)
                        Factory().analyse_file(zf)
                        print(zf.properties)
                        print('Found file:')
                        print(i.internal_attr)

        except Exception as exc:
            print(exc)
            pass
        aojgjbaodga

