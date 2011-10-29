#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       relasync.py
#       Reliable syncronization
#       
#       Copyright 2011 Denis <dderyabin@dderyabin-1>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#
import os
import time
import shutil
import hashlib



from timeit import Timer

###############################################################################
#--------------------------- Configuration -----------------------------------#
###############################################################################

SRC_DIR="/home/dderyabin/sync/src"

DST_DIRS=["/home/dderyabin/sync/dst1",
          "/home/dderyabin/sync/dst2",
          "/home/dderyabin/sync/dst3"]


MD5_FILE = "check.md5"


# Block size for file reading (md5 function)
#BLOCK_SIZE=10240
BLOCK_SIZE=4096
###############################################################################
#---------------------------------- DATA -------------------------------------#
###############################################################################
dFILE_LIST = []

###############################################################################
#-----------------------------------Code--------------------------------------#
###############################################################################

#-----------------------------------------------------------------------------#
# get_md5 - calculates md5 sum for a file
#-----------------------------------------------------------------------------#
def get_md5(filename):
    f = open(filename,'rb')
    m = hashlib.md5()
    while True:
        ## Don't read the entire file at once...
        data = f.read(BLOCK_SIZE)
        if len(data) == 0:
            break
        m.update(data)
    res = m.hexdigest()
    print res   
    return res
#-----------------------------------------------------------------------------#
# dir_walk - go through a path
#-----------------------------------------------------------------------------#
def dir_walk(path):
    for root, dirs, files in os.walk(path):        
        #print "root: %s; dirs:%s"% (root, dirs)
        print "SUB: %s\n\n" % (root.replace(path,""))
        for infile in files:
            f = open(os.path.join(root,infile),'rb')
            filehash = hashlib.md5()
            while True:
                data = f.read(10240)
                if len(data) == 0:
                    break
                filehash.update(data)
            
            #print "%s =>%s" % (os.path.join(root,infile), filehash.hexdigest())

#-----------------------------------------------------------------------------#
# iter_file_list - file list iterator, go through the list of a files
#-----------------------------------------------------------------------------#
def iter_file_list(path):
    result = []
    for root, dirs, files in os.walk(path):        
        for infile in files:
            f = os.path.join(root,infile)
            yield f

#-----------------------------------------------------------------------------#
# add_file
#-----------------------------------------------------------------------------#
def add_file(filename, md5):
    f = open(MD5_FILE,"a")
    f.write("%s;%s" % (md5, filename))
    f.close()


#-----------------------------------------------------------------------------#
# check_file
#-----------------------------------------------------------------------------#
def check_file(filename, md5):
    pass


#-----------------------------------------------------------------------------#
# do_backup
#-----------------------------------------------------------------------------#
def do_backup():
    for filename in iter_file_list(SRC_DIR):
        src_md5 =get_md5(filename)
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

def main():    
    t1 = time.time()
    do_backup()
    t2 = time.time()
    print("Total time:%s" % str(t2-t1))
    return 0

if __name__ == '__main__':
    main()

