#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import shutil

from conf import logger
from checksums import Checksum

from timeit import Timer

# dFILE_LIST = []


def dir_walk(path):
    """dir_walk - go through a path"""
    for root, dirs, files in os.walk(path):        
        # print "root: %s; dirs:%s"% (root, dirs)
        print "SUB: %s\n\n" % (root.replace(path,""))
        for infile in files:
            f = open(os.path.join(root, infile), 'rb')
            filehash = hashlib.md5()
            while True:
                data = f.read(10240)
                if len(data) == 0:
                    break
                filehash.update(data)
            
            #print "%s =>%s" % (os.path.join(root,infile), filehash.hexdigest())


def iter_file_list(path):
    """iter_file_list - file list iterator, go through the list of a files"""
    for root, dirs, files in os.walk(path):
        for infile in files:
            f = os.path.join(root,infile)
            yield f


def add_file(filename, md5):
    f = open(MD5_FILE,"a")
    f.write("%s;%s" % (md5, filename))
    f.close()


def check_file(filename, md5):
    pass


def do_backup():
    for filename in iter_file_list(SRC_DIR):
        src_md5 = get_md5(filename)
        for dst_dir in DST_DIRS:
            dst_file = filename.replace(SRC_DIR,dst_dir)
            if os.path.lexists(dst_file):
                print "file exist"
                # Check MD5 for dst file here
            else:                
                print "Copy '%s' to '%s'" % (filename, dst_file)
                if os.path.isfile(filename):
                    if not os.path.lexists(os.path.split(dst_file)[0]):
                        os.makedirs(os.path.split(dst_file)[0])
                    shutil.copyfile(filename, dst_file)
                else:
                    if not os.path.lexists(dst_file):
                        os.makedirs(dst_file)
                # Check MD5 for dst file here

def check_sfv_file(filename):
    filepath = os.path.split(filename)
    checker = Checksum(filename)
    with open(filename) as sfv:
        for line in sfv:
            orig_hash, path = line.split()
            full_path = os.path.join(filepath, path)
            curr_hash = checker.get_from_file(full_path)
            if curr_hash != orig_hash:
                logger.warning("File hash invalid. "
                               "Filename: '{}' file hash: '{}', "
                               "check hash: '{}'".format(
                    full_path, curr_hash, orig_hash))


def processor(args):
    if args.action == 'check':
        checkfile = args.filename
        check_sfv_file(checkfile)
    t1 = time.time()
    do_backup()
    t2 = time.time()
    print("Total time:%s" % str(t2-t1))
    return 0

