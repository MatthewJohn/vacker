
from vacker.analyser.file.file import File


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


