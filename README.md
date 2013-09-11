m3uco.py
=======
Version: 1.0 beta

A simple command tool that copies all the files from m3u playlists to a specified folder
creating a separate subfolder for each playlist.

USE CASE:



USAGE:


m3uco.py [-h] [--destination DIR] [--rename] [--numbering] [--flat]
                playlists [playlists ...]


  playlists             Playlist files separated by spaces


  -h, --help            show this help message and exit
  --destination DIR, -d DIR
                        Destination directory
  --rename, -r          Renames files in the target directory according to
                        this pattern <artist> - <title>.
  --numbering, -n       Add numbering to rename files, so that the rename
                        pattern becomes <#> <artist> - <title>. Requires
                        --rename option.
  --flat, -f            Prevents from creating a subdirectory for each
                        playlist.

