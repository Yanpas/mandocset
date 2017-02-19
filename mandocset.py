'''
Created on 19 feb 2017

@author: yanpas
'''

import sqlite3, argparse, os, sys, re
from shutil import rmtree

def getPlist(name):
	return '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleIdentifier</key>
	<string>{0}</string>
	<key>CFBundleName</key>
	<string>{0}</string>
	<key>DocSetPlatformFamily</key>
	<string>{0}</string>
	<key>isDashDocset</key>
	<true/>
</dict>
</plist>
'''.format(name)

def toHtml(inf, outdir):
	import subprocess
	name = os.path.basename(inf)
	outfile = os.path.join(outdir, name) + '.html'
	proc = subprocess.Popen(['man2html', inf, '-M', ''], stdout=subprocess.PIPE)
	with open(outfile, 'wb') as f:
		f.write(proc.stdout.read())

def getType(numstr):
	n = int(numstr)
	if n == 1:
		return 'Command'
	elif n == 2:
		return 'Callback'
	elif n == 3:
		return 'Function'
	else:
		return 'Object'

def createDocset(indir, out):
	os.makedirs(out + '.docset/Contents/Resources/Documents')
	with open(out + '.docset/Contents/Info.plist', 'w') as plist:
		plist.write(getPlist(out))
	with sqlite3.connect(out + '.docset/Contents/Resources/docSet.dsidx') as db:
		db.execute("BEGIN")
		db.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
		db.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')
		fldre = re.compile(r'\w*(\d)\w*')
		manfre = re.compile(r'(.+?)\..*')
		for it in os.listdir(indir):
			path1 = os.path.join(indir, it)
			if os.path.isdir(path1):
				mo = re.match(fldre, it)
				if mo:
					print('dir', it)
					for jt in os.listdir(path1):
						manf = os.path.join(path1, jt)
						if os.path.isfile(manf):
							print('\tmanf', jt)
							toHtml(manf, out + '.docset/Contents/Resources/Documents')
							fname = os.path.basename(manf) + '.html'
							name_for_db = re.match(manfre, fname).group(1)
							db.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?);',
									[name_for_db, getType(mo.group(1)), fname])
		db.commit()

def main():
	if os.name != 'posix':
		print('only posix is supported')
		sys.exit(1)
	argp = argparse.ArgumentParser()
	argp.add_argument('-p', '--path', help='path with unpacked archive', required=True)
	argp.add_argument('-o', '--out', help='outpath', required=True)
	argp.add_argument('-f', help='force outdir', type=bool, default=True)
	args = argp.parse_args()
	if os.path.exists(args.out + '.docset'):
		if args.f:
			rmtree(args.out + '.docset')
		else:
			print('path already exists, exiting')
			sys.exit(1)
	createDocset(args.path, args.out)
	
if __name__ == '__main__':
	main()
