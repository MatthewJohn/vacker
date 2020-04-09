
from vacker.analyser.analysers.base import BaseAnalyser


class GeolocationAnalyser(BaseAnalyser):

    @classmethod
    def _convert_to_degress(cls, value):
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

    @classmethod
    def _convert_gps_to_lang_lat(cls, exif_gps):
        latitude = exif_gps.get('GPSLatitude')
        latitude_ref = exif_gps.get('GPSLatitudeRef')
        longitude = exif_gps.get('GPSLongitude')
        longitude_ref = exif_gps.get('GPSLongitudeRef')
        if latitude:
            lat_value = cls._convert_to_degress(latitude)
            if latitude_ref != 'N':
                lat_value = -lat_value
        else:
            return {}
        if longitude:
            lon_value = cls._convert_to_degress(longitude)
            if longitude_ref != 'E':
                lon_value = -lon_value
        else:
            return {}
        return {'latitude': lat_value, 'longitude': lon_value}

    @classmethod
    def check_match(cls, file_obj):
        return False
