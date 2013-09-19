m3uco.py
=======
Version: 1.0 beta

A simple command tool that copies files from a m3u playlist(s) to a destination directory. Useful for transferring
music in playlists to another computer. By defauft sub-directories are created for each playlst. Additional options 
allow to flatten a directory structure or rename files according to their ID3 tags.




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

  --numbering, -n       Add numbering to new file names, so that the rename
                        pattern becomes <#> <artist> - <title>. Requires
                        --rename option.

  --flat, -f            Prevents from creating a subdirectory for each
                        playlist.


