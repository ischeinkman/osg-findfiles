#!/usr/bin/env python3

import os 
import sys

def append_path(path, dest = None):
    if dest is None:
        print("%s"%(path))
    elif 'list' in str(type(dest)):
        dest.append(path)
    else:
        dest.write("%s\n"%(path))

def find_files(destination, cur_path, max_files, cur_files = 0):
    if max_files <= cur_files:
        return cur_files
    entries = os.listdir(cur_path)
    subdirs = []
    for itm in entries:
        if itm[0] == '.':
            continue
        if cur_files >= max_files:
            break
        abspath = os.path.join(cur_path, itm)
        if os.path.isfile(abspath):
            append_path(abspath, destination)
            cur_files += 1
        elif os.path.isdir(abspath):
            subdirs.append(abspath)
    for subdir in subdirs:
        if cur_files >= max_files:
            break 
        cur_files = find_files(destination, subdir, max_files, cur_files)
    return cur_files

def print_help():
    print(""" 
        findfiles -- recursively finds files in a directory up to a given number. 
        Format:
        \t findfiles [-n MAXFILES] [--out FILE] [path]

        Flags:

        -n\t the maximum number of files to be returned
        -o | --out\t the file location to store output. Defaults to stdout. 
    """)


def main(argv):
    if '--help' in  argv:
        print_help()
        return 
    print("Setting default args")
    
    dest_name = None 
    max_files = 2**32 - 1
    path = os.getcwd()
    print("Parsing flags")
    for idx in range(0, len(argv)):
        if argv[idx][-3:] == '.py':
            continue
        if argv[idx] == '-o' or argv[idx] == '--out':
            dest_name = argv[idx + 1]
            idx += 1 
        elif argv[idx] == '-n':
            max_files = int(argv[idx+1])
            idx += 1
        else:
            path = argv[idx]
    print('Now searching in directory %s'%(path))
    if dest_name is None:
        dest = None 
    elif dest_name == 'list':
        dest = []
    else:
        dest = open(dest_name, 'w')
    found = find_files(dest, path, max_files)
    print('Found %d files.'%(found))

print(list(map(lambda fn: fn[-3:], sys.argv)))
main(sys.argv)