import os
import sys
import codecs
import hashlib
import logging

from conf import get_conf, get_logger
from helpers import timeit


class ChecksumMD5(object):

    @staticmethod
    def get_from_file(filename):
        """get_md5 - calculates md5 sum for a file"""
        # system_encoding = sys.getfilesystemencoding()
        # f = open(filename.decode(system_encoding), "rb")
        f = open(filename, mode='rb')
        m = hashlib.md5()
        block_size = get_conf()['checksum']['md5']['block_size']
        while True:
            # Don't read the entire file at once...
            data = f.read(block_size)
            if len(data) == 0:
                break
            m.update(data)
        res = m.hexdigest()
        return res


class ChecksumXXHASH(object):
    @staticmethod
    def get_from_file(filename):
        assert NotImplementedError
        return ''


class Checksum(object):
    def __init__(self, filename):
        self.hash_filename = filename
        file_base, file_ext = os.path.splitext(filename)
        if file_ext == '.md5':
            self.processor = ChecksumMD5()
        elif file_ext == '.xxhash':
            self.processor = ChecksumXXHASH()
        else:
            raise Exception, "Unknown checksum file type: %s" % filename

    def check(self):
        DEBUG = get_logger().getEffectiveLevel() == logging.DEBUG
        base_path, filename = os.path.split(self.hash_filename)
        invalids = []
        with codecs.open(self.hash_filename, encoding='utf-8') as sfv:
            for line in sfv:
                orig_hash, path = line.split()
                full_path = os.path.join(base_path, path)
                curr_hash = self.get_from_file(full_path)
                if DEBUG:
                    get_logger().debug("Current hash: '{}', orig hash: '{}'.".format(curr_hash, orig_hash))
                if curr_hash != orig_hash:
                    get_logger().warning("File hash invalid. "
                                         "Filename: '{}' file hash: '{}', "
                                         "check hash: '{}'".format(
                        full_path.encode(encoding='utf-8'),
                        curr_hash,
                        orig_hash))
                    invalids.append({
                        'curr_hash': curr_hash,
                        'orig_hash': orig_hash,
                        'filename': full_path
                    })
        return invalids

    @timeit
    def get_from_file(self, filename):
        return self.processor.get_from_file(filename)
