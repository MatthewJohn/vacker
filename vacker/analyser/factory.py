
from vacker.analyser.analysers import *
from vacker.analyser.file import File


class Factory(object):

    ANALYSIS_CLASSES = None

    @staticmethod
    def get_analysis_classes(base_cls):
        if Factory.ANALYSIS_CLASSES is None:
            classes = []

            def add_sub_classes(sub_class):
                for sub_class_itx in sub_class.__subclasses__():
                    classes.append(sub_class_itx)
                    add_sub_classes(sub_class_itx)

            add_sub_classes(base_cls)
            Factory.ANALYSIS_CLASSES = classes

        return Factory.ANALYSIS_CLASSES

    @staticmethod
    def analyse_file(file_obj):

        for cls_itx in [BaseAnalyser] + Factory.get_analysis_classes(BaseAnalyser):
            if cls_itx.check_match(file_obj):
                cls_itx.get_file_properties(file_obj)

        return [file_obj] + file_obj.additional_files
