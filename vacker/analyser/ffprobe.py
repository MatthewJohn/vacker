
import subprocess
import json

from vacker.analyser.base import BaseAnalyser


class FfprobeAnalyser(BaseAnalyser):

    @staticmethod
    def _get_ffprobe_data(file_obj):
        try:
            return json.loads(subprocess.check_output(['ffprobe', file_obj.path, '-print_format', 'json', '-show_format', '-show_streams']))
        except (subprocess.CalledProcessError, ) as exc:
            print('Error during ffprobe: {0}'.format(str(exc)))
            return {}

    @classmethod
    def _get_ffprobe_analysis(cls, file_obj, audio_only=False):
        ffprobe_props = cls._get_ffprobe_data(file_obj)
        analysed_props = {}

        analysed_props['m_length'] = int(float(ffprobe_props['format']['duration']))
        analysed_props['v_container'] = ffprobe_props['format']['format_long_name']

        for prop, tag in [['m_creation_time', 'creation_time'],
                          ['m_title', 'title'],
                          ['m_comment', 'comment'],
                          ['a_artist', 'artist'],
                          ['a_track', 'track'],
                          ['a_album', 'album'],
                          ['a_album_artist', 'album_artist']]:
            if tag in ffprobe_props['format']['tags']:
                analysed_props[prop] = ffprobe_props['format']['tags'][tag]

        v = 0
        a = 0
        for stream in ffprobe_props['streams']:
            pref = None
            if stream['codec_type'] == 'video' and not audio_only:
                # Take audio details from first found video stream (as generally it
                # will be the primary)
                if not v:
                    analysed_props['pv_width'] = stream['width']
                    analysed_props['pv_height'] = stream['height']
                    fr_a, fr_b = stream['r_frame_rate'].split('/')
                    analysed_props['v_frame_rate'] = int(int(fr_a) / int(fr_b))
                    pref = 'v'
                v += 1

            elif stream['codec_type'] == 'audio':
                # Take audio details from first found audio stream (as generally it
                # will be the primary)
                if not a:
                    analysed_props['a_sample_rate'] = stream['sample_rate']
                    analysed_props['a_channels'] = stream['channels']
                    pref = 'a'
                a += 1

            else:
                # Unrecognised stream
                continue

            if 'codec_name' in stream:
                analysed_props['{0}_codec'.format(pref)] = stream['codec_name']
            if 'bit_rate' in stream:
                analysed_props['{0}_bitrate'.format(pref)] = stream['bit_rate']

        return analysed_props, ffprobe_props


    @classmethod
    def check_match(cls, file_obj):
        return False
