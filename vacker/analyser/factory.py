
from vacker.analyser import *
from vacker.analyser.file import File


class Factory(object):

    ANALYSIS_CLASSES = None

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
    def analyse_file(file_path):
        file_obj = File(file_path)

        cls = BaseAnalyser
        for cls_itx in Factory.get_analysis_classes(BaseAnalyser):
            if cls_itx.check_match(file_obj):
                cls = cls_itx

        for cls_itx in [cls] + [cls_ for cls_ in cls.__bases__]:
            if cls_itx is object:
                continue
            cls_itx.get_file_properties(file_obj)

        return file_obj
