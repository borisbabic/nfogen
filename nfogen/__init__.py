#!/usr/bin/env python2

from tvdb_api import Tvdb
from tvdb_exceptions import tvdb_shownotfound
import re
import sys
import os

t=Tvdb(True)



DIRECTORY_SLASH = '\\' if os.name =='nt' else '/'

BASE_URL = 'http://thetvdb.com/?tab=series&id={tv_show_id}&lid=7'
TV_SHOW_NFO = 'tvshow_nfo'
MATCH_YEAR = re.compile('\(\d+\)')
FAILED = []
SUCCESS = []
SKIPPED = []

def create_url(tv_show_id):
    return BASE_URL.format(tv_show_id=tv_show_id)

def add_slash(directory):
    if (directory[-1] != DIRECTORY_SLASH):
        directory += DIRECTORY_SLASH
    return directory

def create_file(directory, url):
    directory = add_slash(directory)
    file_name = directory + TV_SHOW_NFO
    with open(file_name, 'w') as nfo_file:
        nfo_file.write(url)
        print "Writing " +  url + " to " + file_name

def create_nfo(tv_dir, true_dir = False):

    if (true_dir == False):
        true_dir = tv_dir
    try:
        tv_show = t[tv_dir]
        url = create_url(tv_show['id'])
        create_file(true_dir, url)
        SUCCESS.append(tv_dir)
    except tvdb_shownotfound:
        print "\nCan't find anything for" + tv_dir
        without_year, match = MATCH_YEAR.subn('', tv_dir)
        if (match > 0):
            print "Trying " + without_year
            create_nfo(without_year, tv_dir)
        else:
            FAILED.append(tv_dir)

def print_particular_result(particular, name):
    length = len(particular)
    print "======================="
    print "{0}: {1}".format(name, length)
    if (length > 0):
        print ""
        for tv_show in particular:
            print tv_show

def print_result():
    print "\n======================="
    print "========RESULTS========"
    print_particular_result(SUCCESS, 'Success')
    print_particular_result(SKIPPED, 'Skipped')
    print_particular_result(FAILED, 'Failed')

def main():
    base_directory = add_slash(sys.argv[-1])
    print "Searching " + base_directory
    if (not os.path.isdir(base_directory)):
        print "%(dir)s is not a directory!" % {'dir': base_directory}
        exit(3)

    os.chdir(base_directory)
    tv_directories = filter(os.path.isdir, os.listdir('.' + DIRECTORY_SLASH))
    for tv_dir in tv_directories:
        print "======================\nSearching for: " + tv_dir
        if (os.path.exists(add_slash(tv_dir) + TV_SHOW_NFO)):
            print tv_dir + " already has a " + TV_SHOW_NFO
            SKIPPED.append(tv_dir)
        else:
            create_nfo(tv_dir)
    print_result()


if __name__ == '__main__':
    main()
