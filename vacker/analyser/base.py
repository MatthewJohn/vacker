import os
import hashlib
import uuid

class BaseAnalyser(object):


    @classmethod
    def get_file_properties(cls, file_obj):
        file_obj.properties['id'] = uuid.uuid4()
        file_obj.properties['g_size'] = int(os.path.getsize(file_obj.path))
        file_obj.properties['g_path'] = file_obj.path
        file_obj.properties['g_file_name'] = file_obj.path.split('/')[-1]
        file_obj.properties['g_directory'] = '/'.join(file_obj.path.split('/')[0:-1])
        file_obj.properties['g_mime_type'] = file_obj.mime_type

        (file_obj.properties['g_sha1'],
         file_obj.properties['g_sha512']) = cls.get_checksums(file_obj)

        file_obj.properties['g_extension'] = (
            file_obj.properties['g_file_name'].split('.')[-1]
            if '.' in file_obj.properties['g_file_name'] else '')


    @staticmethod
    def get_checksums(file_obj):
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
        if cls is BaseAnalyser:
            return file_obj.__class__.__name__ == 'File'

        raise NotImplementedError
