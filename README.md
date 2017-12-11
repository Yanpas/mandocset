# mandocset

This is python script (mandocset.py) that generates Dash docset from man pages. It takes folders with man pages as it's arguments. Then in each folder it finds all folders, containing digit in their name, runs `man2html -r` for each file inside them.

### Some links to man pages
* [manpages-posix](https://launchpad.net/ubuntu/+source/manpages-posix)
* linux man pages' [git](https://www.kernel.org/doc/man-pages/)

How to run: `python3 mandocset.py -o Linux_Man_Pages -p resourse/man-pages-4.09/ resourse/man-pages-posix-2013-a/ -i etc/tux.png -I etc/tux@2x.png`. You may also view help: `python3 mandocset.py -h`.

### Looking for linux manpages docset?
1. Download `etc/Linux.docset.zip` from this repo
2. Extract it to Linux.docset folder
3. Move this folder to Zeal docsets (`C:\Users\%username%\AppData\Local\Zeal\Zeal\docsets` or `~/.local/share/Zeal/Zeal/docsets/`)
