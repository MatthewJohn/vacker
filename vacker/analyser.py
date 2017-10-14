
from mimetypes import MimeTypes
import PIL.ExifTags
import PIL.Image
import hashlib
from datetime import datetime

class MediaType(object):
    UNSUPPORTED = 0
    PHOTO = 1
    VIDEO = 2

class Analyser(object):

    def detect_media_type(self, path):
        mime = MimeTypes()
        object_mime_type = mime.guess_type(path)[0]
        if object_mime_type is None:
            return MediaType.UNSUPPORTED

        if object_mime_type.split('/')[0] == 'image':
            return MediaType.PHOTO
        if object_mime_type.split('/')[0] == 'video':
            return MediaType.VIDEO
        else:
            return MediaType.UNSUPPORTED

    def get_image_data(self, path):
        pil_image = PIL.Image.open(path)
        image_info = {'datetime': None, 'orientation': None}
        gps_info = {}
        if hasattr(pil_image, '_getexif'):
            exif_data = {
              PIL.ExifTags.TAGS[k]: v
              for k, v in pil_image._getexif().items()
              if k in PIL.ExifTags.TAGS
            }
            if 'Orientation' in exif_data:
                image_info['orientation'] = exif_data['Orientation']
            if 'GPSInfo' in exif_data:
                for key in exif_data['GPSInfo'].keys():
                    decode = PIL.ExifTags.GPSTAGS.get(key,key)
                    gps_info[decode] = exif_data['GPSInfo'][key]
                long_lat = self._convert_gps_to_lang_lat(gps_info)
                if 'longitude' in long_lat and 'latitude' in long_lat:
                    image_info['location'] = {'type': 'Point', 'coordinates': [ long_lat['longitude'], long_lat['latitude']]}
            for datetime_tag in ['DateTime',
                                 'DateTimeOriginal',
                                 'DateTimeDigitized']:
                if datetime_tag in exif_data:
                    try:
                        image_info['datetime'] = datetime.strptime(exif_data[datetime_tag], '%Y:%m:%d %H:%M:%S')
                        break
                    except:
                        pass
        image_info['width'], image_info['height'] = pil_image.size
        pil_image.close()
        return image_info

    def _convert_to_degress(self, value):
        """
        Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
        :param value:
        :type value: exifread.utils.Ratio
        :rtype: float
        """
        d = float(value[0][0]) / float(value[0][1])
        m = float(value[1][0]) / float(value[1][1])
        s = float(value[2][0]) / float(value[2][1])

        return d + (m / 60.0) + (s / 3600.0)

    def _convert_gps_to_lang_lat(self, exif_gps):
        latitude = exif_gps.get('GPSLatitude')
        latitude_ref = exif_gps.get('GPSLatitudeRef')
        longitude = exif_gps.get('GPSLongitude')
        longitude_ref = exif_gps.get('GPSLongitudeRef')
        if latitude:
            lat_value = self._convert_to_degress(latitude)
            if latitude_ref != 'N':
                lat_value = -lat_value
        else:
            return {}
        if longitude:
            lon_value = self._convert_to_degress(longitude)
            if longitude_ref != 'E':
                lon_value = -lon_value
        else:
            return {}
        return {'latitude': lat_value, 'longitude': lon_value}

    def get_video_data(self, path):
        pass

    def get_checksum(self, path):
        block_size = 2**20
        md5 = hashlib.md5()
        with open(path, 'rb') as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()
