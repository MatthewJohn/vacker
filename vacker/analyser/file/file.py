
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


