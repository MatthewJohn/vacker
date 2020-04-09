
import magic
import os


class File(object):

    def __init__(self, path):
        """Store basic member variables."""
        self._path = path
        self._mime_type = None
        self._size = None
        self.properties = {}
        self._is_symlink = None
        self._additional_files = []

    def additional_file(self, additional_file):
        """Add file to list of additional files to analyse."""
        self._additional_files.append(additional_file)

    @property
    def additional_files(self):
        """Obtain list of all additional accumulated files."""
        return self._additional_files

    @property
    def mime_type(self):
        """Determine mimetype of file."""
        if self._mime_type is None:
            with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
                with self.get_file_handle() as fh:
                    self._mime_type = m.id_buffer(fh.read(8 * 8))

        return self._mime_type

    def get_file_handle(self, mode='rb'):
        """Obtain filehandle to file."""
        return open(self._path, mode)

    @property
    def size(self):
        """Determine size of file."""
        if self._size is None:
            self._size = int(os.path.getsize(self.path))
        return self._size

    @property
    def path(self):
        """Return path of file."""
        return self._path

    @property
    def is_virtual(self):
        """Is the file virtual..."""
        return False

    @property
    def is_symlink(self):
        """Determine if file is symlink."""
        if self._is_symlink is None:
            self._is_symlink = os.path.islink(self.path)
        return self._is_symlink


class VirtualFile(File):

    @property
    def is_virtual(self):
        return True

    @property
    def is_symlink(self):
        """."""
        # Don't treat virtual files as symlinks
        # TODO: Test this works
        return False


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


class TarredFile(VirtualFile):

    def __init__(self, parent_tar, tar_object):
        self._parent_tar = parent_tar
        self._tar_object = tar_object
        super(TarredFile, self).__init__(self.generate_filename())

    def generate_filename(self):
        """Generate file path, including original tar."""
        return '{0}/{1}'.format(self._parent_tar.filename,
                                self._tar_object.name)

    def get_file_handle(self, mode='r'):
        return self._parent_tar.extractfile(self._tar_object)

    @property
    def size(self):
        """Get object size."""
        return self.tar_object.size

    @property
    def parent_tar(self):
        """Get file object for parent tar file."""
        return self._parent_tar

    @property
    def tar_object(self):
        return self._tar_object


