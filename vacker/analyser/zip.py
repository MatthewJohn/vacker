
from datetime import datetime
import zipfile

from vacker.analyser.base import BaseAnalyser
from vacker.analyser.factory import Factory
from vacker.analyser.file import ZippedFile


class ZipAnalyser(BaseAnalyser):


    @staticmethod
    def check_match(file_obj):
        return (
            not file_obj.is_symlink and
            file_obj.mime_type == 'application/zip' and
            file_obj.__class__.__name__ == 'File'
        )

    @classmethod
    def get_file_properties(cls, file_obj):
        try:
            zip_content = (file_obj.get_file_handle(mode='r') if file_obj.__class__.__name__ == 'ZippedFile' else file_obj.path)
            with zipfile.ZipFile(zip_content) as myzip:

                for i in myzip.infolist():
                    if not i.is_dir():
                        zf = ZippedFile(myzip, i)
                        Factory().analyse_file(zf)
                        file_obj.additional_file(zf)

        except Exception as exc:
            print(exc)
