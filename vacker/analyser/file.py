
import magic


class File(object):

    def __init__(self, path):
        self._path = path
        self._mime_type = None
        self.properties = {}
        self._additional_files = []

    def additional_file(self, additional_file):
        self._additional_files.append(additional_file)

    @property
    def additional_files(self):
        return self._additional_files    

    @property
    def mime_type(self):
        if self._mime_type is None:
            with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
                with self.get_file_handle() as fh:
                    self._mime_type = m.id_buffer(fh.read())

        return self._mime_type

    def get_file_handle(self, mode='rb'):
        fh = open(self._path, mode)
        return fh
    
    @property
    def path(self):
        return self._path


class ZippedFile(File):

    def __init__(self, parent_zip, zip_object):
        self._parent_zip = parent_zip
        self._zip_object = zip_object
        super(ZippedFile, self).__init__(self.generate_filename())

    def generate_filename(self):
        return '{0}/{1}'.format(self._parent_zip.filename, self._zip_object.filename)

    def get_file_handle(self, mode='r'):
        fh = self._parent_zip.open(self._zip_object, mode=mode)
        fh.name = self._zip_object.filename
        return fh

    @property
    def path(self):
        return self._path

    @property
    def parent_zip(self):
        return self._parent_zip

    @property
    def zip_object(self):
        return self._zip_object

