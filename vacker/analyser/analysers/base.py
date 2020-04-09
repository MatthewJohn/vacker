
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

