
from vacker.analyser.file.virtual_file import VirtualFile


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


