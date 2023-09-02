# mandocset

This is a Python script ([`mandocset.py`](mandocset.py)) that generates a Dash docset from man pages. It takes folders with man pages as its arguments. Then in each folder it finds all folders containing digit in their name, and runs `man2html -r` for each file inside them.

By default the script uses the `man2html` utility, which should be available from your distro's package manager. If you prefer [Pandoc][1], add `-e "pandoc -f man -t html"` to the command line.

## How to run

```bash
python3 mandocset.py -o Linux_Man_Pages -p resource/man-pages-4.09/ resource/man-pages-posix-2013-a/ -i etc/tux.png -I etc/tux@2x.png
```

Then copy or move the generated `Linux_Man_Pages.docset` to `~/.local/share/Zeal/Zeal/docsets` or `%APPDATA%\Local\Zeal\Zeal\docsets` on Windows.

You may also view help: `python3 mandocset.py -h`.

### Looking for a pre-built Linux manpages docset?

1. Download [`etc/Linux.docset.zip`](/blob/master/etc/Linux.docset.zip) from this repo
2. Extract it to `Linux.docset` folder
3. Move this folder to `%APPDATA%\Local\Zeal\Zeal\docsets` on Windows or `~/.local/share/Zeal/Zeal/docsets/` on Linux

### Generating a docset from your system's installed manpages

You can generate a docset of all manpages on your system (the script supports manpages compressed with gzip or bzip2). Usually these are located at `/usr/share/man`.

On a reasonably well-equipped Linux system, the [included Makefile](Makefile) can do this for you:

```bash
cd ~/path/where/you/cloned/Yanpas/mandocset
make  # or 'make docset'

# if the above works OK
make install

# print what would happen, but don't actually do it
make install DRYRUN=1

# remove the previously-built docset
make reallyclean

# specify custom docset name and search shortcut (or just modify the Makefile)
make install DOCSETNAME='Linux manpages' SHORTCUT=man
```

Look inside [the Makefile](Makefile) for other configurable settings.

## Some links to man pages

* [manpages-posix][2]
* Linux man pages' [Git repository][3]

[1]: https://pandoc.org
[2]: https://launchpad.net/ubuntu/+source/manpages-posix
[3]: https://www.kernel.org/doc/man-pages
