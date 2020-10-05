

from vacker.analyser.ffprobe import FfprobeAnalyser


class VideoAnalyser(FfprobeAnalyser):


    @staticmethod
    def check_match(file_obj):
        return (file_obj.mime_type and
                file_obj.mime_type.split('/')[0] == 'video' and
                file_obj.__class__.__name__ not in ['ZippedFile', 'TarredFile'])

    @classmethod
    def generate_thumbnail(cls, file_obj):
        """Generate thumbnail for image."""
        try:
            pil_image = PIL.Image.open(file_obj.path)
            pil_image.thumbnail(cls.THUMBNAIL_SIZE)
            pil_image.save(file_obj.get_thumbnail_path(), "JPEG")
        except (OSError, ValueError) as exc:
            print('Failed to generate image thumbnail: ' + str(exc))
            return

    @classmethod
    def get_file_properties(cls, file_obj):
        ffprobe_props, ffprobe_raw_props = cls._get_ffprobe_analysis(file_obj)
        file_obj.properties.update(ffprobe_props)

        #print(ffprobe_props)
