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

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

logger.info("Python version: " + sys.version)

def parse_args():
    parser = argparse.ArgumentParser(description='A simple tool that copies all the files from m3u playlists to a target folder.')
    parser.add_argument('playlists', help='Playlist files separated by spaces', nargs='+')
    parser.add_argument('--destination', '-d', metavar='DIR', help='Destination directory', default=os.getcwd())
    parser.add_argument('--rename', '-r',  help='Renames files in the target directory according to this pattern <artist> - <title>.',
        action='store_true', default=False)
    parser.add_argument('--numbering', '-n', help='Add numbering to new file names, so that the rename pattern becomes <#> <artist> - <title>. Requires --rename option.',
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
                print "\nProcessing %s" % file
                target = args.destination

                if not args.flat: #put files into subdirectories
                    playlist_name = os.path.basename(file)
                    if playlist_name.endswith(".m3u"):
                        playlist_name = playlist_name[:-4]
                    target = os.path.join(args.destination, playlist_name)

                if not os.path.isdir(target):
                    os.makedirs(target)

                print "\t%d files copied, %d files skipped." % copy_m3u(m3u, target, args.rename, args.numbering)

        except IOError as e:
            logger.critical(e);
            #logger.critical(" Playlist 404: %s" % file)


def copy_m3u(m3u, target, is_rename, is_numbering):
    n = 1
    copied = 0
    skipped = 0

    for line in m3u:
        if line.strip()[0] != "#":
            src =  os.path.abspath(line.decode('utf-8-sig').strip())

            logger.debug("Entry: %s" % line)
            logger.debug("Abspath: %s" % src)

            if os.path.exists(src):
                filename = os.path.basename(src)

                if is_rename and rename(src, is_numbering, n):
                    filename = rename(src, is_numbering, n)
                    
                n = n + 1

                dst = os.path.join(target, filename)
                logger.debug("Destination: %s" % dst)

                #halt if source is fresher than destination
                if os.path.exists(dst) and os.stat(src).st_mtime - os.stat(dst).st_mtime < 1:
                    logger.info("File exists. Skipping.")
                    skipped = skipped + 1
                    continue

                shutil.copy2 (src, dst)
                copied = copied + 1
            else:
                logger.error(" File 404: %s" % src)

    return (copied, skipped)


def rename(src, is_numbering = False, n=None):
    try:
        logger.info("Path exists")
        id3r = id3reader.Reader(src)
        artist = id3r.getValue("performer")
        title = id3r.getValue("title")

        if artist is None or title is None:
            return None

        if is_numbering and n != None:
            filename = "%02d %s - %s" % (n, artist, title) + os.path.splitext(src)[1]
        else:
            filename = "%s - %s" % (artist, title) + os.path.splitext(src)[1]

        logger.info("New filename: " + filename)
        return sanitize(filename) if artist and title else src
        

    except:
        return None


def sanitize(filename):
    validchars = ",.()+-_;' "
    filename = filename.replace("\"", "''").replace("\\", "-").replace("/", "+").replace(":", "-")
    return "".join(c for c in filename if c.isalnum() or c in validchars).rstrip();


if __name__ == "__main__":
    main(parse_args())
