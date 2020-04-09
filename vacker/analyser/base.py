import os
import hashlib
import uuid
import subprocess


class BaseAnalyser(object):
    """Provide base checks for anything on filesystem."""

    SHAMEAN_BIN = '/usr/local/bin/shamean'

    @classmethod
    def get_file_properties(cls, file_obj):
        """Get basic file properties."""
        file_obj.properties['id'] = uuid.uuid4()
        file_obj.properties['g_path'] = file_obj.path
        file_obj.properties['g_file_name'] = file_obj.path.split('/')[-1]
        file_obj.properties['g_directory'] = '/'.join(file_obj.path.split('/')[0:-1])
        file_obj.properties['g_file_type'] = file_obj.__class__.__name__

        file_obj.properties['g_extension'] = (
            file_obj.properties['g_file_name'].split('.')[-1]
            if '.' in file_obj.properties['g_file_name'] else '')

    @classmethod
    def check_match(cls, file_obj):
        """Base method to determine if file is applicable to analyser.
        Only non-inheritted analyser classes should return True."""
        # Base class is always applicable to standard files
        if cls is BaseAnalyser:
            return True

        raise NotImplementedError


class BaseFile(BaseAnalyser):
    """Perform checks on real files."""

    SHAMEAN_BIN = '/usr/local/bin/shamean'

    @classmethod
    def get_file_properties(cls, file_obj):
        """Get basic file properties."""
        file_obj.properties['g_mime_type'] = file_obj.mime_type

        file_obj.properties['g_shamean'] = (
            cls.get_shamean(file_obj)
            if not file_obj.is_virtual else None
        )

        file_obj.properties['g_size'] = file_obj.size

    @staticmethod
    def get_shamean(file_obj):
        """Get shamean checksum"""
        return subprocess.check_output([BaseAnalyser.SHAMEAN_BIN, file_obj.path]).strip()

    @staticmethod
    def get_checksums(file_obj):
        """Get sha1 and sha512 checksums"""
        block_size = 2**20
        sha512 = hashlib.sha512()
        sha1 = hashlib.sha1()
        with file_obj.get_file_handle() as fh_:
            while True:
                data = fh_.read(block_size)
                if not data:
                    break
                sha512.update(data)
                sha1.update(data)
        return sha1.hexdigest(), sha512.hexdigest()

    @classmethod
    def check_match(cls, file_obj):
        """Base method to determine if file is applicable to analyser.
        Only non-inheritted analyser classes should return True."""
        # Base class is always applicable to standard files
        return not file_obj.is_symlink
