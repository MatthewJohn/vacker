
import PIL
import StringIO
from bson.objectid import ObjectId
from bson.binary import Binary


from vacker.media import Media
import vacker.database

class Photo(Media):

    def create_thumbnail(self):
        pil_image = PIL.Image.open(self.get_path())
        orientation = self.get_orientation()
        if orientation == 3:
            pil_image = pil_image.rotate(180, expand=True)
        elif orientation == 6:
            pil_image = pil_image.rotate(270, expand=True)
        elif orientation == 8:
            pil_image = pil_image.rotate(90, expand=True)
        try:
            pil_image.thumbnail((300, 300), PIL.Image.ANTIALIAS)
            output = StringIO.StringIO()
            pil_image.save(output, 'JPEG')
            contents = output.getvalue()
            output.close()
            db = vacker.database.Database.get_database()
            db.thumbnail.insert_one({'_id': ObjectId(self.get_id()), 'thumbnail_data': Binary(contents)})
        except:
            print 'Error creating thumbnail: %s' % self.get_path()
            raise

    def get_photo_data(self):
        with open(self.get_path(), 'rb') as rh:
            data = rh.read()
        return data
