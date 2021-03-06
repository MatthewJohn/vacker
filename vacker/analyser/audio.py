

from vacker.analyser.ffprobe import FfprobeAnalyser


class AudioAnalyser(FfprobeAnalyser):


    @staticmethod
    def check_match(file_obj):
        return (file_obj.mime_type and
                file_obj.mime_type.split('/')[0] == 'audio' and
                file_obj.__class__.__name__ not in ['ZippedFile', 'TarredFile'])

    @classmethod
    def get_file_properties(cls, file_obj):
        ffprobe_props, ffprobe_raw_props = cls._get_ffprobe_analysis(file_obj, audio_only=True)
        file_obj.properties.update(ffprobe_props)
