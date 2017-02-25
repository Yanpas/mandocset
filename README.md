# mandocset

python script mandocset.py takes folders with man pages. Then in each folder it finds all folders, containing digit in their name, then runs `man2html -r` util for each file inside them.

Posix man pages were taken from ubuntu's package [manpages-posix](https://launchpad.net/ubuntu/+source/manpages-posix)
linux man pages were taken from linux's [git](https://www.kernel.org/doc/man-pages/)

How to run: `python3 mandocset.py -o Linux_Man_Pages -p resourse/man-pages-4.09/ resourse/man-pages-posix-2013-a/ -i etc/tux.png -I etc/tux@2x.png`
