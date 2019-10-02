
from mimetypes import MimeTypes


class File(object):

    def __init__(self, path):
        self._path = path
        self._mime_type = None
        self.properties = {}

    @property
    def mime_type(self):
        if self._mime_type is None:
            self._mime_type = MimeTypes().guess_type(self._path)
        return self._mime_type
    
    @property
    def path(self):
        return self._path
