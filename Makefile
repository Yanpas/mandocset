##
##  usage:
##    $ make install
##

MANPAGES = /usr/share/man
DOCSETSDIR = $(HOME)/.local/share/Zeal/Zeal/docsets
DOCSETNAME = Linux Man Pages
# the supplied DOCSETNAME, with spaces replaced by underscores
DOCSETNAME_ = $(subst $(null) $(null),_,$(DOCSETNAME))
# workaround to allow subst'ing a space, since it normally trims whitespace
null =
# if not supplied, mandocset.py defaults to first word of DOCSETNAME_, split on underscores
#SHORTCUT = man
ICON = etc/tux.png
ICON2X = $(ICON:.png=@2x.png)
MAYBEDO = $(if $(DRYRUN),echo)


docset: $(DOCSETNAME_).docset/Contents/Info.plist

install: $(DOCSETSDIR)/$(DOCSETNAME_).docset/Contents/Info.plist

clean:
	$(MAYBEDO) rm -rf $(DOCSETNAME_).docset

reallyclean: clean
	$(MAYBEDO) rm -rf $(DOCSETSDIR)/$(DOCSETNAME_).docset

$(DOCSETNAME_).docset/Contents/Info.plist:
	$(MAYBEDO) python3 mandocset.py -o $(DOCSETNAME_) -i $(ICON) -I $(ICON2X) -p $(MANPAGES)
ifneq ($(SHORTCUT),)
	$(MAYBEDO) sed -i "/DocSetPlatformFamily/{N;s^<string>.*</string>^<string>$(SHORTCUT)</string>^;}" $@
endif

# use 'cp -r' here if you don't have 'rsync' installed
$(DOCSETSDIR)/$(DOCSETNAME_).docset/Contents/Info.plist: $(DOCSETNAME_).docset/Contents/Info.plist
	$(MAYBEDO) rsync -av --delete $(DOCSETNAME_).docset $(DOCSETSDIR)
