
from datetime import datetime
import tarfile

from vacker.analyser.analysers.base import BaseAnalyser
from vacker.analyser.analysers.factory import Factory
from vacker.analyser.file import TarredFile


class TarAnalyser(BaseAnalyser):


    @staticmethod
    def check_match(file_obj):
        is_tar = False
        try:
            is_tar = tarfile.is_tarfile(file_obj.path)
        except:
            pass

        return (
            not file_obj.is_symlink and
            file_obj.__class__.__name__ == 'File' and
            is_tar
        )

    @classmethod
    def get_file_properties(cls, file_obj):
        try:
            with tarfile.open(file_obj.path) as tar:
                tar.filename = file_obj.path
                for i in tar.getmembers():
                    if i.isfile():
                        print(i.name)
                        tf = TarredFile(tar, i)
                        Factory().analyse_file(tf)
                        file_obj.additional_file(tf)

        except Exception as exc:
            print(exc)

