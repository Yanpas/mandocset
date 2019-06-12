#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 19 feb 2017

DocsetMaker

@author: yanpas
'''

import sqlite3, argparse, os, re, subprocess, sys
import shutil
from typing import List

def getPlist(name: str) -> str:
	return '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleIdentifier</key>
	<string>{}</string>
	<key>CFBundleName</key>
	<string>{}</string>
	<key>DocSetPlatformFamily</key>
	<string>{}</string>
	<key>isDashDocset</key>
	<true/>
</dict>
</plist>
'''.format(name.split('_')[0],
		name.replace('_', ' '),
		name.split('_')[0].lower())

def toHtml(executable: List[str], inf: str, outdir: str, basedir: str):
	name = os.path.basename(inf)
	inf_f = open(inf)
	for suff, decoder in [('.gz', 'gzip'), ('.bz2', 'bzip2')]:
		if inf.endswith(suff):
			name = ''.join(name.rsplit(suff, 1))
			inf_f = subprocess.Popen([decoder, '-d'], stdin=inf_f, stdout=subprocess.PIPE).stdout
			break
	subp = subprocess.Popen(executable, stdout=subprocess.PIPE, stdin=inf_f)
	subp.stdout.readline() # skip Content-Type http header
	outpath = os.path.join(basedir, name) + '.html'
	with open(os.path.join(outdir, outpath), 'wb') as f:
		f.write(subp.stdout.read())
	if subp.wait() != 0:
		print(executable[0], "error:", subp.returncode, file=sys.stderr)
	return outpath

def getType(n):
	if n == 1:
		return 'Command'
	elif n == 2:
		return 'Service' # Command and Callback have too similar icons
	elif n == 3:
		return 'Function'
	else:
		return 'Object'

class DocsetMaker:
	fldre  = re.compile(r'\w*(\d)\w*')
	manfre = re.compile(r'(.+)\..*?\d.*')

	def __init__(self, outname, executable: str):
		self.outname = outname
		self.dups = set()
		self.db = None
		self.executable = executable.split()

	def __enter__(self):
		os.makedirs(self.outname + '.docset/Contents/Resources/Documents')
		self.db = sqlite3.connect(self.outname + '.docset/Contents/Resources/docSet.dsidx')
		self.db.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
		self.db.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')
		with open(self.outname + '.docset/Contents/Info.plist', 'w') as plist:
			plist.write(getPlist(self.outname))
		return self

	def __exit__(self, *oth):
		self.db.close()

	def scanDirectory(self, path1, it, mannum):
		outbase = self.outname + '.docset/Contents/Resources/Documents'
		os.makedirs(os.path.join(outbase, it), exist_ok=True)
		for jt in os.listdir(path1):
			manf = os.path.join(path1, jt)
			if os.path.isfile(manf) and re.match(DocsetMaker.manfre, jt):
				print('\tman', jt)
				fname = os.path.join(it, os.path.basename(manf)) + '.html'
				name_for_db = re.match(DocsetMaker.manfre, jt).group(1)
				dashtype = getType(mannum)
				new_el = (mannum, name_for_db)
				if not (new_el in self.dups):
					outpath = toHtml(self.executable, manf, outbase, it)
					self.db.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?);',
							[name_for_db, dashtype, outpath])
					self.dups.add(new_el)
				else:
					print('\tduplicate skipped',fname)

	def addToDocset(self, indir):
		self.db.execute("BEGIN")
		for it in os.listdir(indir):
			path1 = os.path.join(indir, it)
			if os.path.isdir(path1):
				mo = re.match(DocsetMaker.fldre, it)
				if mo:
					print('dir', it)
					self.scanDirectory(path1, it, int(mo.group(1)))
		self.db.commit()

def main():
	argp = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	argp.add_argument('-p', '--paths', help='paths with unpacked archive, order matters', nargs='+', required=True)
	argp.add_argument('-o', '--out', help='new docset name', required=True)
	argp.add_argument('-f', help='force outdir', action='store_true')
	argp.add_argument('-i', help='x1 icon (16x16)', metavar='icon.png')
	argp.add_argument('-I', help='x2 icon (32x32)', metavar='icon@2x.png')
	argp.add_argument('-e', default='man2html -r',
		help=('Executable with arguments which reads from stdin and writes to stdout.'
			' Alterntaively "pandoc -f man -t html" may be used'))
	args = argp.parse_args()
	if ' ' in args.out:
		exit('spaces are forbidden in outname')
	outpath = args.out + '.docset'
	if os.path.exists(outpath):
		if args.f:
			shutil.rmtree(outpath)
		else:
			exit('path already exists, exiting (use "-f" to ignore this)')
	with DocsetMaker(args.out, args.e) as dsm:
		for path in args.paths:
			dsm.addToDocset(path)
	for name,path in [('icon.png', args.i), ('icon@2x.png', args.I)]:
		if path:
			shutil.copyfile(path, os.path.join(outpath, name))

if __name__ == '__main__':
	main()
