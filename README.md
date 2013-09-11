m3uco.py
=======
Version: 1.0 beta

A simple command tool that copies all the files from m3u playlists to a specified directory
creating a separate subdir for each playlist. Additional options allow to flatten directory 
structure or rename files according to their ID3 tags. The tool is useful for consolidating
your playlists into a neat directory structure with all the files present in a specified
location for an easy transfer.



USAGE
=======

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

