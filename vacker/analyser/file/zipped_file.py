
from vacker.analyser.file.virtual_file import VirtualFile


class ZippedFile(VirtualFile):

    def __init__(self, parent_zip, zip_object):
        self._parent_zip = parent_zip
        self._zip_object = zip_object
        super(ZippedFile, self).__init__(self.generate_filename())

    def generate_filename(self):
        """Generate file path, including original zip."""
        return '{0}/{1}'.format(self._parent_zip.filename,
                                self._zip_object.filename)

    def get_file_handle(self, mode='r'):
        """Obtain filehandle object"""
        file_handle = self._parent_zip.open(self._zip_object, mode=mode)
        file_handle.name = self._zip_object.filename
        return file_handle

    @property
    def size(self):
        return int(self.zip_object.file_size)

    @property
    def parent_zip(self):
        return self._parent_zip

    @property
    def zip_object(self):
        return self._zip_object

