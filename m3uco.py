__author__ = 'roman'
"""
m3uco.py
Version: 1.0 beta

A simple command tool that copies all the files from m3u playlists to a specified folder
creating a separate subfolder for each playlist.


===========================================================================

The MIT License (MIT)

Copyright (c) 2013 Roman Sirokov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import argparse
import os
import sys
import shutil
import id3reader
import logging
from glob import glob

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Python version: " + sys.version)

def parse_args():
    parser = argparse.ArgumentParser(description='A simple tool that copies all the files from m3u playlists to a target folder.')
    parser.add_argument('playlists', help='Playlist files separated by spaces', nargs='+')
    parser.add_argument('--destination', '-d', metavar='DIR', help='Destination directory', default=os.getcwd())
    parser.add_argument('--rename', '-r',  help='Renames files in the target directory according to this pattern <artist> - <title>.',
        action='store_true', default=False)
    parser.add_argument('--numbering', '-n', help='Add numbering to rename files, so that the rename pattern becomes <#> <artist> - <title>. Requires --rename option.',
        action='store_true', default=False)
    parser.add_argument('--flat', '-f', help='Prevents from creating a subdirectory for each playlist.', action='store_true', default=False)

    return parser.parse_args()



def main(args):
    logger.debug(args)

    filenames = []
    for arg in args.playlists:
        for filename in glob(arg):
            filenames.append(filename)

    logger.debug(filenames)

    for file in set(filenames):
        try:
            with open(file, "rU") as m3u:
                target = args.destination

                if not args.flat: #put files into subdirectories
                    playlist_name = os.path.basename(file)
                    if playlist_name.endswith(".m3u"):
                        playlist_name = playlist_name[:-4]
                    target = os.path.join(args.destination, playlist_name)

                if not os.path.isdir(target):
                    os.makedirs(target)

                copy_m3u(m3u, target, args.rename, args.numbering)

        except IOError:
            logger.error(" File 404: %s")


def copy_m3u(m3u, target, is_rename, is_numbering):
    n = 1

    for line in m3u:
        if line[0] != "#":
            src = os.path.abspath(line.strip())

            logger.debug("Entry: %s" % line)
            logger.debug("Abspath: %s" % src)

            if os.path.exists(src):
                filename = os.path.basename(src)

                if is_rename:
                    filename = rename(src, is_numbering)

                dst = os.path.join(target, filename)
                logger.debug("Destination: %s" % dst)

                #halt if source is fresher than destination
                if os.path.exists(dst) and os.stat(src).st_mtime - os.stat(dst).st_mtime < 1:
                    logger.info("File exists. Skipping.")
                    continue

                shutil.copy2 (src, dst)
            else:
                logger.error(" File 404: %s" % src)


        n = n + 1


def rename(src, is_numbering):
    try:
        logger.info("Path exists")
        id3r = id3reader.Reader(src)
        artist = id3r.getValue("performer")
        title = id3r.getValue("title")

        if is_numbering:
            filename = "%02d %s - %s" % (n, artist, title) + os.path.splitext(src)[1]
        else:
            filename = "%s - %s" % (artist, title) + os.path.splitext(src)[1]

        logger.info("New filename: " + filename)
        return filename if artist and title else src

    except TypeError:
        return None


if __name__ == "__main__":
    main(parse_args())
