
from datetime import datetime

import PIL.ExifTags
import PIL.Image

from vacker.analyser.geolocation import GeolocationAnalyser


class ImageAnalyser(GeolocationAnalyser):


    @staticmethod
    def check_match(file_obj):

        return file_obj.mime_type[0] and file_obj.mime_type[0].split('/')[0] == 'image'

    @classmethod
    def get_file_properties(cls, file_obj):
        try:
            pil_image = PIL.Image.open(file_obj.path)
        except OSError as exc:
            print(str(exc))
            return

        file_obj.properties['pv_date_taken'] = None
        file_obj.properties['pv_orientation'] = None
        gps_info = {}
        if hasattr(pil_image, '_getexif'):
            exif_data = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in pil_image._getexif().items()
                if k in PIL.ExifTags.TAGS
            } if pil_image._getexif() else None

            if exif_data:
                if 'Orientation' in exif_data:
                    file_obj.properties['pv_orientation'] = exif_data['Orientation']

                if 'GPSInfo' in exif_data:
                    for key in exif_data['GPSInfo'].keys():
                        decode = PIL.ExifTags.GPSTAGS.get(key,key)
                        gps_info[decode] = exif_data['GPSInfo'][key]

                    long_lat = cls._convert_gps_to_lang_lat(gps_info)

                    if 'longitude' in long_lat and 'latitude' in long_lat and False:
                        file_obj.properties['location'] = {
                            'type': 'Point',
                            'coordinates': [
                                long_lat['longitude'],
                                long_lat['latitude']
                            ]
                        }

                for datetime_tag in ['DateTime',
                                     'DateTimeOriginal',
                                     'DateTimeDigitized']:
                    if datetime_tag in exif_data:
                        try:
                            file_obj.properties['pv_date_taken'] = datetime.strptime(exif_data[datetime_tag], '%Y:%m:%d %H:%M:%S')
                            break
                        except:
                            pass

        file_obj.properties['pv_width'], file_obj.properties['pv_height'] = pil_image.size
        pil_image.close()

        # If the datetime has been obtained from the meta information,
        # split the year, month and day out for easier searching/indexing
        #if 'pv_date_taken' in file_obj.properties and file_obj.properties['pv_date_taken']:
            #file_obj.properties['pv_date_y'] = file_obj.properties['pv_date_taken'].year
            #file_obj.properties['pv_date_m'] = file_obj.properties['pv_date_taken'].month
            #file_obj.properties['pv_date_d'] = file_obj.properties['pv_date_taken'].day
