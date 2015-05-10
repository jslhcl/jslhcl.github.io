---
layout:	post
title:	"Programming Python notes"
date:	2014-12-29
---
# Chapter 2 A Sneak Preview

## Lists
{%highlight python%}
>>> bob = ['Bob Smith', 42, 30000, 'software']
>>> sue = ['Sue Jones', 45, 40000, 'music']
>>> bob[0], sue[2]
('Bob Smith', 40000)

>>> bob[0].split()[-1]
'Smith'

>>> people = [bob,sue]
>>> for person in people:
	print person

>>> people[1][0]
'Sue Jones'

>>> pays = [person[2] for person in people]	# collect all pay
>>> pays
[30000, 40000]
>>> pays = map((lambda x: x[2]), people)	# ditto
>>> sum(person[2] for person in people)
70000

>>> people.append(['Tom', 50, 0, None])
>>> len(people)
3
>>> people[-1][0]
'Tom'

>>> NAME, AGE, PAY = range(3)	#[0,1,2]
>>> bob = ['Bob Smith', 42, 10000]
>>> bob[NAME]
'Bob Smith'

>>> bob = [['name', 'Bob Smith'], ['age', 42], ['pay', 10000]]
>>> sue = [['name', 'Sue Jones'], ['age', 45], ['pay', 20000]]
>>> for person in people:
	print person[0][1], person[2][1]

>>> for person in people:
	for (name, value) in person:
		if name=='name': print value

>>> def field(record, label):	# function
	for (fname, fvalue) in record:
		if fname == label:
			return fvalue
>>> field(bob, 'name')
'Bob Smith'
>>> field(sue, 'pay')
20000
{%endhighlight%}

## Dictionaries

{%highlight python%}
>>> bob = {'name':'Bob Smith', 'age':42, 'pay':30000, 'job':'software'}
>>> sue = {'name':'Sue Jones', 'age':45, 'pay':40000, 'job':'music'}
>>> bob['name'].split()[-1]

>>> bob = dict(name='Bob Smith', age=42, pay=30000, job='dev');
>>> bob
{'pay':30000, 'job':'dev', 'age':42, 'name':'Bob Smith'}
>>> bob['name'], sue['pay']
('Bob Smith', 40000)

>>> bob['name'].split()[-1]
'Smith'

>>> people = [bob,sue]
>>> for person in people:
	print person

>>> people[1][0]
'Sue Jones'

>>> pays = [person[2] for person in people]	# collect all pay
>>> pays
[30000, 40000]
>>> pays = map((lambda x: x[2]), people)	# ditto
>>> sum(person[2] for person in people)
70000

>>> people.append(['Tom', 50, 0, None])
>>> len(people)
3
>>> people[-1][0]
'Tom'

>>> NAME, AGE, PAY = range(3)	#[0,1,2]
>>> bob = ['Bob Smith', 42, 10000]
>>> bob[NAME]
'Bob Smith'

>>> bob = [['name', 'Bob Smith'], ['age', 42], ['pay', 10000]]
>>> sue = [['name', 'Sue Jones'], ['age', 45], ['pay', 20000]]
>>> for person in people:
	print person[0][1], person[2][1]

>>> for person in people:
	for (name, value) in person:
		if name=='name': print value

>>> def field(record, label):	# function
	for (fname, fvalue) in record:
		if fname == label:
			return fvalue
>>> field(bob, 'name')
'Bob Smith'
>>> field(sue, 'pay')
20000

>>> sue = {}
>>> sue['name'] = 'Sue Jones'
>>> sue['age'] = 45
>>> sue['pay'] = 40000
>>> sue['job'] = 'mus'
>>> sue
{'job':'mus', 'pay':40000, 'age':45, 'name':'Sue Jones'}

>>> names = ['name', 'age', 'pay', 'job']
>>> values = ['Sue Jones', 45, 40000, 'mus']
>>> zip(names, values)
[('name', 'Sue Jones'), ('age', 45), ('pay', 40000), ('job', 'mus')]
>>> sue = dict(zip(names, values))
{'job':'mus', 'pay':40000, 'age':45, 'name':'Sue Jones'}

>>> fields = ('name', 'age', 'job', 'pay')
>>> record = dict.fromkeys(fields, '?')
>>> record
{'job':'?', 'pay':'?', 'age':'?', 'name':'?'}

>>> print open('data.txt').read()
001.1 002.2 003.3
010.1 020.2 030.3 040.4
100.1 200.2 300.3
>>> sums = {}
>>> for line in open('data.txt'):
	cols = [float(col) for col in line.split()]
	for pos,val in enumerate(cols):
		sums[pos] = sums.get(pos, 0.0)+val
>>> for key in sorted(sums):
	print key, '=', sums[key]
0=111.3
1=222.6
3=333.9
4=40.4

{%endhighlight%}

## files

{%highlight python%}
# initdata.py

#records
bob = {'name':'Bob Smith', 'age':42, 'pay':30000, 'job':'software'}
sue = {'name':'Sue Jones', 'age':45, 'pay':40000, 'job':'music'}

db = {}
db['bob'] = bob
db['sue'] = sue

if __name__=='__main__':	# when run as a script, true only when this file is run, not when it is imported
	for key in db:
		print key, '=>\n', db[key]


# make_db_files.py
dbfilename = 'people-file'
ENDDB = 'enddb.'
ENDREC = 'endrec.'
RECSEP = '=>'

def storeDbase(db, dbfilename=dbfilename):
	"formatted dump of database to flat file"
	dbfile = open(dbfilename, 'w')
	for key in db:
		print >> dbfile, key
		for (name, value) in db[key].items():
			print >> dbfile, name+RECSEP+repr(value)	#repr(): convert the parameter to string
		print >> dbfile, ENDREC
	print >> dbfile, ENDDB
	dbfile.close()
	
def loadDbase(dbfilename=dbfilename):
	"parse data to reconstruct database"
	dbfile = open(dbfilename)
	import sys
	sys.stdin = dbfile
	db = {}
	key = raw_input()	#get input
	while key != ENDDB:
		rec = {}
		field = raw_input()
		while field != ENDREC:
			name, value = field.split(RECSEP)
			rec[name] = eval(value)	# obj = eval(repr(obj)) 
			field = raw_input()
		db[key] = rec
		key = raw_input()
	return db

if __name__ == '__main__':
	from initdata import db
	storeDbase(db)
				

## dump_db_file.py
from make_db_file import loadDbase
db = loadDbase()
for key in db:
	print key, '=>\n ', db[key]
print db['sue']['name']


## update_db_file.py
from make_db_file import loadDbase, storeDbase
db = loadDbase()
db['sue']['pay] *= 1.10
db['tom']['name'] = 'Tom Tom'
storeDbase(db)
{%endhighlight%}

## pickle files

{%highlight python%}
## make_db_pickle.py
from initdata import db
import pickle
dbfile = open('people-pickle', 'w')
pickle.dump(db, dbfile)
dbfile.close()


## dump_db_pickle.py
import pickle
dbfile = open('people-pickle')
db = pickle.load(dbfile)
for key in db:
	print key, '=>\n ', db[key]
print db['sue']['name']


## make_db_pickle_recs.py
from initdata import bob, sue, tom
import pickle
for (key, record) in [('bob', bob), ('tom', tom), ('sue', sue)]:
	recfile = open(key+'.pkl', w)
	pickle.dump(record, recfile)
	recfile.close()


## dump_db_pickle_recs.py
import pickle, glob
for filename in glob.glob('*.pkl'):
	recfile = open(filename)
	record = pickle.load(recfile)
	print filename, '=>\n ', record

suefile = open('sue.pkl')
print pickle.load(suefile)['name']
{%endhighlight%}

## Using Shelves

{%highlight python%}
## make_db_shelve.py
from initdata import bob, sue
import shelve
db = shelve.open('people-shelve')
db['bob'] = bob
db['sue'] = sue
db.close()


## dump_db_shelve.py
import shelve
db = shelve.open('people-shelve')
for key in db:
	print key, '=>\n ' db[key]
print db['sue']['name']
db.close()
{%endhighlight%}

## OOP

{%highlight python%}
## person.py
class Person:
	def __init__(self, name, age, pay=0, job=None):
		self.name = name
		self.age = age
		self.pay = pay
		self.job = job
	
	def lastName(self):
		return self.name.split()[-1]
	
	def giveRaise(self, percent):
		self.pay *= (1.0+percent)

	def __str__(self):
		return '<%s => %s>' % (self.__class__.__name__, self.name)

if __name__ == '__main__':
	bob = Person('Bob Smith', 42, 30000, 'sweng')
	sue = Person('Sue Jones', 45, 40000, 'music')
	print bob.name, sue.pay
	print bob.lastName()
	sue.giveRaise(.10)
	print sue.pay

## manager.py
from person import Person

class Manager(Person):
	def __init__(self, name, age, pay):
		Person.__init__(self, name, age, pay, 'manager')

	def giveRaise(self, percent, bonus=0.1):
		Person.giveRaise(self, percent+bonus)

# the following are equivalent:
# instance.method(arg1, arg2)
# class.method(instance, arg1, arg2)

if __name__ == '__main__':
	tom = Manager('Tom Jones', 50)
	print tom	#<Manager => Tom Jones>

## make_db_classes.py
import shelve
from person import Person
from manager import Manager

bob = Person('Bob Smith', 42, 30000, 'sweng')
sue = Person('Sue Jones', 45, 40000, 'music')
tom = Manager('Tom Jones', 50, 50000)

db = shelve.open('class-shelve')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()

## dump_db_class.py
import shelve
db = shelve.open('class-shelve')
for key in db:
	print key, '=>\n ', db[key].name, db[key].pay
{%endhighlight%}

## interaction

{%highlight python%}
## peopleinteract_query.py
import shelve 
fieldnames = ('name', 'age', 'job', 'pay')
maxfield = max(len(f) for f in fieldnames)
db = shelve.open('class-shelve')

while True:
	key = raw_input('\nKey? => ')	#key or empty line, exc at eof
	if not key: break
	try:
		record = db[key]
	except:
		print 'No such key "%s"!' % key
	else:
		for field in fieldnames:
			print field.ljust(maxfield), '=>', getattr(record, field)

## peopleinteract_update.py
import shelve
from person import Person
fieldnames = ('name', 'age', 'job', 'pay')

db = shelve.open('class-shelve')
while True:
	key = raw_input('\nKey? => ')
	if not key: break
	if key in db.keys():
		record = db[key]
	else:
		record = Person(name='?', age='?')
	for field in fieldnames:
		currval = getattr(record, field)
		newtext = raw_input('\t[%s]=%s\n\t\tnew?=>' % (field, currval))
		if newtext:
			setattr(record, field, eval(newtext))
	db[key] = record
db.close()

{%endhighlight%}

## GUI

{%highlight python%}
##tkinter001.py
from Tkinter import *
Label(text='Spam').pack()
mainloop()

##tkinter101.py
from Tkinter import *
from tkMessageBox import showinfo

def reply():
	showinfo(title='popup', message='button pressed!')

window = Tk()
button = Button(window, text='press', command=reply)
button.pack()
window.mainloop()

##tkinter102.py
from Tkinter import *
from tkMessageBox import showinfo

class MyGui(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		button = Button(self, text='press', command=self.reply)
		button.pack()
	def reply(self):
		showinfo(title='popup', message='Button pressed!')

if __name__ == '__main__':
	window = MyGui()
	window.pack()
	window.mainloop()

## attachgui.py
from Tkinter import *
from tkinter102 import MyGui

# main app window
mainwin = Tk()
Label(mainwin, text=__name__).pack()

# popup window
popup = Toplevel()
Label(popup, text='Attach').pack(side=LEFT)
MyGui(popup).pack(side=RIGHT)
mainwin.mainloop()

## customizegui.py
from tkMessageBox import showinfo
from tkinter102 import MyGui

class CustomGui(MyGui):
	def reply(self):
		showinfo(title='popup', message='Ouch!')

if __name__ == '__main__':
	CustomGui().pack()
	mainloop()

## tkinter103.py
from Tkinter import *
from tkMessageBox import showinfo

def reply(name):
	showinfo(title='Reply', message='Hello %s!' % name)

top = Tk()
top.title('Echo')
#top.iconbitmap('py-blue-trans-out.ico')

Label(top, text="Enter your name:").pack(side=TOP)
ent = Entry(top)
ent.pack(side=TOP)
btn = Button(top, text="Submit", command=(lambda: reply(ent.get())))
btn.pack(side=LEFT)

top.mainloop()

## peoplegui.py
from Tkinter import *
from tkMessageBox import showerror
import shelve
shelvename = 'class-shelve'
fieldnames = ('name', 'age', 'job', 'pay')

def makeWidgets():
	global entries
	window = Tk()
	window.title('People Shelve')
	form = Frame(window)
	labels = Frame(form)
	values = Frame(form)
	labels.pack(side=LEFT)
	values.pack(side=RIGHT)
	form.pack()
	entries = {}
	for label in ('key',)+fieldnames:
		Label(labels, text=label).pack()
		ent = Entry(values)
		ent.pack()
		entries[label] = ent
	Button(window, text="Fetch", command=fetchRecord).pack(side=LEFT)
	Button(window, text="Update", command=updateRecord).pack(side=LEFT)
	Button(window, text="Quit", command=window.quit).pack(side=RIGHT)
	return window

def fetchRecord():
	key = entries['key'].get()
	try:
		record = db[key]
	except:
		showerror(title='Error', message='No Such Key!')
	else:
		for field in fieldnames:
			entries[field].delete(0,END)
			entries[field].insert(0, repr(getattr(record, field)))

def updateRecord():
	key = entries['key'].get()
	if key in db.keys():
		record = db[key]
	else:
		from person import Person
		record = Person(name='?', age='?')
	for field in fieldnames:
		setattr(record, field, eval(entries[field].get()))
	db[key] = record

db = shelve.open(shelvename)
window = makeWidgets()
window = mainloop()
db.close()
	
{%endhighlight%}

## Web Interface

{%highlight python%}
## webserver.py
webdir = '.'
port = 80

import os, sys
from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler

if sys.platform[:3] == 'win':
	CGIHTTPRequestHandler.have_popen2 = False
	CGIHTTPRequestHandler.have_popen3 = False

os.chdir(webdir)
srvraddr = ("", port)
srvrobj = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()

## cgi101.html
<html>
<title>Interactive Page</title>
<body>
<form method=POST action="cgi-bin/cgi101.py">
	<p><B>Enter your name:</B>
	<p><input type=text name=user>
	<p><input type=submit>
</form>
</body></html>

## cgi101.py
#!/usr/bin/python
import cgi
form = cgi.FieldStorage()
print "Content-type: text/html\n"
print "<title>Reply Page</title>"
if not form.has_key('user'):
	print "<h1>Who are you?</h1>"
else:
	print "<h1>Hello <i>%s</i>!</h1>" % cgi.escape(form['user'].value)

## command line
>>> from urllib import urlopen
>>> conn = urlopen('http://localhost/cgi-bin/cgi101.py?user=Sue+Smith')
>>> reply = conn.read()
>>> reply
'<title>Reply Page</title>\n<h1>Hello <i>Sue Smith</i>!</h1>\n'


## peoplecgi.html
<html>
<title>People Input Form</title>
<body>
<form method=POST action="cgi-bin/peoplecgi.py">
	<table>
	<tr><th>Key  <td><input type=text name=key>
	<tr><th>Name <td><input type=text name=name>
	<tr><th>Age  <td><input type=text name=age>
	<tr><th>Job  <td><input type=text name=job>
	<tr><th>Pay  <td><input type=text name=pay>
	</table>
	<p>
	<input type=submit value="Fetch", name=action>
	<input type=submit value="Update", name=action>
</form>
</body></html>


## peoplecgi.py, 'Permission denied' when executing db = shelve.open()
#!/usr/bin/python
import cgi, shelve
from person import Person
form = cgi.FieldStorage()
print "Content-type: text/html"
shelvename = 'class-shelve'
fieldnames = ('name', 'age', 'job', 'pay')

replyhtml = """
<html>
<title>People Input Form</title>
<body>
<form method=POST action="peoplecgi.py">
	<table>
	<tr><th>Key  <td><input type=text name=key value="%(key)s">
	$ROWS$
	</table>
	<p>
	<input type=submit value="Fetch", name=action>
	<input type=submit value="Update", name=action>
</form>
</body></html>
"""

rowhtml = '<tr><th>%s<td><input type=text name=%s value="%%(%s)s">\n'
rowshtml = ''
for fieldname in fieldnames:
	rowshtml += (rowhtml % ((fieldname,) *3))
replyhtml = replyhtml.replace('$ROWS$', rowshtml)

def htmlize(adict):
	new = adict.copy()
	for field in fieldnames:
		value = new[field]
		new[field] = cgi.escape(repr(value))
	return new

def fetchRecord(db, form):
	try:
		key = form['key'].value
		record = db[key]
		fields = record.__dict__
		fields['key'] = key
	except:
		fields = dict.fromkeys(fieldnames, '?')
		fields['key'] = 'Missing or invalid key!'
	return fields

def updateRecord(db, form):
	if not form.has_key('key'):
		fields = dict.fromkeys(fieldnames, '?')
		fields['key'] = 'Missing key input!'
	else:
		key = form['key'].value
		if key in db.keys():
			record = db[key]
		else:
			record = Person(name='?', age='?')
		for field in fieldnames:
			setattr(record, field, eval(form[field].value))
		db[key] = record
		fields = record.__dict__
		fields['key'] = key
	return fields

db = shelve.open(shelvename)
#bob = Person('Bob Smith', 42, 30000, 'sweng')
#sue = Person('Sue Jones', 45, 40000, 'music')
#tom = Manager('Tom Jones', 50, 50000)

#db = {}#shelve.open('class-shelve')
#db['bob'] = bob
#db['sue'] = sue
#db['tom'] = tom


action = form.has_key('action') and form['action'].value
if action == 'Fetch':
	fields = fetchRecord(db, form)
elif action == 'Update':
	fields = updateRecord(db, form)
else:
	fields = dict.fromkeys(fieldnames, '?')
	fields['key'] = 'Missing or invalid action!'
db.close()
print replyhtml % htmlize(fields)

#if __name__ == '__main__':
#	db = shelve.open(shelvename)
#	print 'in main'
#	print db['bob']
#	db.close()
{%endhighlight%}

# Chapter 3 System Tools

{%highlight python%}
## more.py
def more(text, numlines=15):
	lines = text.split('\n')
	while lines:
		chunk = lines[:numlines]
		lines = lines[numlines:]
		for line in chunk: print line
		if lines and raw_input('More?) not in ['y', 'Y']: break

if __name__ == '__main__':
	import sys
	more(open(sys.argv[1]).read(), 10)

## command line
>>> str = 'SHRUBBERY'
>>> str.lower()
'shrubbery'
>>> str.isalpha()
>>> str.isdigit()
>>> import string
>>> string.lowercase
>>> str = 'aaa,bbb,ccc'
>>> str.split(',')
['aaa', 'bbb', 'ccc']
>>> str = 'a b\nc\nd'
>>> str.split()
['a','b','c','d']
>>> delim = 'NI'
>>> delim.join(['aaa','bbb','ccc'])
>>> 'aaaNIbbbNIccc'
>>> ' '.join(['A', 'dead', 'parrot'])
'A dead parrot'
>>> chars = list('Lorreta')
['L','o','r','r','e','t','a']
>>> chars.append('!')
>>> ''.join(chars)
'Lorreta!'

>>> str = 'xxaaxxaa'
>>> 'SPAM'.join(str.split('aa'))	# replace, the hard way
'xxSPAMxxSPAM'

>>> int("42"), eval("42")	# string to int
(42, 42)
>>> str(42), repr(42), ("%d" % 42)	# int to string
('42', '42', '42')
>>> "42"+str(1), int("42")+1	# add
('421', 43)

>>> import sys	# system info
>>> sys.platform, sys.maxint, sys.version, sys.path

## os Module
>>> os.getpid()
>>> os.getcmd()
>>> os.chdir(r'c:\tmp')	# r means do not escape
>>> os.pathsep, os.sep, os.pardir, os.curdir, os.linesep
>>> os.path.isdir(r'C:\temp'),	os.path.isfile(r'C:\temp')
(True, False)
>>> os.path.exists(r'C:\temp\data.txt')
0
>>> os.path.getsize(r'C:\autoexec.bat')
260
>>> os.path.split(r'C:\temp\data.txt')
('C:\\temp', 'data.txt')
>>> os.path.join(r'C:\temp', 'output.txt')
'C:\\temp\\output.txt'

>>> name = r'C:\temp\data.txt'
>>> os.path.basename(name), os.path.dirname(name)	# Windows paths
('data.txt', 'C:\\temp')

import os
os.system('dir /B'), os.system('type helloshell.py')

>>> open('helloshell.py').read()
>>> text = os.popen('type helloshell.py').read()	# os.popen also connects to the standard input or output streams of the command
>>> listing = os.popen('dir /B').readlines()

# When os.system and os.popen are called, they must start a brand-new, independent program running on your operating system (they generally run the command in a newly forked process)

## testargv.py
import sys
print sys.argv

## command line test
>>> python testargv.py -i data.txt -o result.txt
['testargv.py', '-i', 'data.txt', '-o', 'result.txt']

# parse arguments library: getopt, optparse

## Shell Environment Variables
>>> import os
>>> os.environ.keys(), os.environ['TEMP']

# it's worth pointing out that it can be made a bit less machine dependent by listing the Unix env command at the top instead of a hardcoded path to the Python executable:

#!/usr/bin/env python
print 'Wait for it...'
{%endhighlight%}

Key assignments change both the os.environ object in the Python program as well as the associated variable in the enclosing shell environment of the running program's process. Its new value becomes visible to the Python program, all linked-in C modules, and any programs spawned by the Python process.

{%highlight python%}
## setenv.py
import os
print 'setenv...'
print os.environ['USER']

os.environ['USER'] = 'Brian'
os.system('python echoenv.py')

os.environ['USER'] = 'Arthur'
os.system('python echoenv.py')

os.environ['USER'] = raw_input('?')
print os.popen('python echoenv.py').read()

## echoenv.py
import os
print 'echoenv...'
print 'Hello, ', os.environ['USER']

{%endhighlight%}

## Redirect, pipes
{%highlight python%}
## teststreams.py
def interact():
	print 'Hello stream world'
	while 1:
		try:
			reply = raw_input('Enter a number>')
		except EOFError:
			break
		else:
			num = int(reply)
			print "%d squared is %d" % (num, num ** 2)
	print 'Bye'

if __name__ == '__main__':
	interact()

## command line
>>> python teststreams.py < input.txt > output.txt
>>> python teststreams.py < input.txt | more

## moreplus.py
import sys
def getreply():
	if sys.stdin.isatty():		# if stdin is console
		return raw_input('?')	
	else:
		if sys.platform[:3] == 'win':	# if stdin was redirected
			import msvcrt
			msvcrt.putch('?')
			key = msvcrt.getche()
			msvcrt.putch('\n')
			return key
		elif sys.platform[:5] == 'linux':	# use linux console device
			print '?'
			console = open('/dev/tty')
			line = console.readline()[:-1]	#strip eoln at line end
			return line
		else:
			print '[pause]'
			import time
			time.sleep(5)
			return 'y'

def more(text, numlines=10):
	lines = text.split('\n')
	while lines:
		chunk = lines[:numlines]
		lines = lines[numlines:]
		for line in chunk: print line
		if lines and getreply() not in ['y', 'Y']: break

if __name__ == '__main__':
	if len(sys.argv) == 1:
		more(sys.stdin.read())
	else:
		more(open(sys.argv[1]).read())
{%endhighlight%}

## Redirecting streams to Python Objects
{%highlight python%}
## redirect.py

import sys
class Output:
	def __init__(self):
		self.text = ''
	def write(self, string):
		self.text = self.text+string
	def writelines(self, lines):
		for line in lines: self.write(line)

class Input:
	def __init__(self, input=''):
		self.text = input
	def read(self, *size):	#size is a variable argument list, http://blog.csdn.net/chenjinyu_tang/article/details/8136841
		if not size:
			res, self.text = self.text, ''
		else:
			res, self.text = self.text[:size[0]], self.text[size[0]:]
		return res
	def readline(self):
		eoln = self.text.find('\n')
		if eoln == -1:
			res, self.text = self.text, ''
		else:
			res, self.text = self.text[:eoln+1], self.text[eoln+1:]
		return res
	def redirect(function, args, input):
		savestreams = sys.stdin, sys.stdout
		sys.stdin = Input(input)
		sys.stdout= Output()
		try:
			function(*args)
		except:
			sys.stderr.write('error in function! ')
			sys.stderr.write('%s, %s\n' % tuple(sys.exc_info()[:2]))
		result = sys.stdout.text
		sys.stdin, sys.stdout = savestreams
		return result

## command line
>>> from teststreams import interact
>>> interact()
Hello stream world
Enter a number>2
2 squared is 4
Enter a number>3
3 squared is 9
Enter a number

>>> from redirect import redirect
>>> output = redirect(interact, (), '4\n5\n')
>>> output
'Hello stream world\nEnter a number>4 squared is 16\nEnter a number>5 squared is 25\nEnter a number>Bye\n'

## StringIO Module
>>> from StringIO import StringIO
>>> buff = StringIO()
>>> buff.write('spam\n')
>>> buff.write('eggs\n')
>>> buff.getvalues()
'spam\neggs\n'

>>> buff = StringIO('ham\nspam\n')
>>> buff.readline()
'ham\n'
>>> buff.readline()
'spam\n'
>>> buff.readline()
''

>>> from StringIO import StringIO
>>> import sys
>>> buff = StringIO()

>>> temp = sys.stdout
>>> sys.stdout = buff
>>> print 42, 'spam', 3.141

>>> sys.stdout = temp
>>> buff.getvalue()
'42 spam 3.141\n'

# 2>&1 means redirect the standard error to standard output

## Other Redirection Options
## hello-out.py
print 'Hello shell world'

## hello-in.py
input = raw_input()
open('hello-in.txt', 'w').write('Hello '+input+'\n')

## command line
>>> import os
>>> pipe = os.popen('python hello-out.py')	#'r' is default--read output
>>> pipe.read()
'Hello shell world\n'

>>> pipe = os.popen('python hello-in.py', 'w')
>>> pipe.write('Gumby\n')
>>> pipe.close()
>>> open('hello-in.txt').read()
Hello Gumby\n'
{%endhighlight%}

# Chapter 4 File and Directory Tools

## parse packed binary data with the struct module

{%highlight python%}
>>>import struct
>>> data = struct.pack('>i4shf', 2, 'spam', 3, 1.234)	# '>i4shf' means big-endian(>), an integer, four-character string, half integer, and float

>>> file = open('data.bin', 'wb')
>>> file.write(data)
>>> file.close()

>>> file = open('data.bin', 'rb')
>>> bytes = file.read()
>>> values = struct.unpack('>i4shf', data)
>>> values
(2, 'spam', 3, 1.23399996)
{%endhighlight%}

## Running shell listing commands with os.popen

{%highlight python%}
>>> import os
>>> os.popen('dir /B').readlines()
['about-p.html\n', 'python1.5.tar.gz\n', ...]
{%endhighlight%}

## The glob module

{%highlight python%}
>>> import glob
>>> glob.glob('*.html')
['about-pp.html', 'about-pp2e.html', 'about-ppr2e.html']
{%endhighlight%}

## Walking Directory Trees

{%highlight python%}
>>> import os
>>> def lister(dummy, dirname, filesindir):
	print '['+ dirname + ']'
	for fname in filesindir:
		print os.path.join(dirname, fname)

>>> os.path.walk('.', lister, None)

>>> matches = []
>>> for (dirname, dirshere, fileshere) in os.walk(r'D:\PP3E'):
	for filename in fileshere:
		if filename.endswith('.py'):
			pathname = os.path.join(dirname, filename)
			if 'Tkinter' in open(pathname).read():
				matches.append(pathname)

## lister_recur.py
import sys, os

def mylister(currdir):
	print '[' + currdir + ']'
	for file in os.listdir(currdir):
		path = os.path.join(currdir, file)
		if not os.path.isdir(path):
			print path
		else:
			mylister(path)

if __name__ == '__main__':
	mylister(sys.argv[1])
{%endhighlight%}

## Rolling your own find Module

{%highlight python%}
## find.py
#!/usr/bin/python
import fnmatch, os

def find(pattern, startdir=os.curdir):
	matches = []
	os.path.walk(startdir, findvisitor, (matches, pattern))
	matches.sort()
	return matches
	
def findvisitor((matches, pattern), thisdir, nameshere):
	for name in nameshere:
		if fnmatch.fnmatch(name, pattern):
			fullpath = os.path.join(thisdir, name)
			matches.append(fullpath)
			
if __name__ == '__main__':
	import sys
	namepattern, startdir = sys.argv[1], sys.argv[2]
	for name in find(namepattern, startdir): print name 

## usage:
# python find.py *.py .| more

# for name in find.find('*.py'):
#	...do something with name...
{%endhighlight%}

# Chapter 5 Parallel System Tools

## Fork

{%highlight python%}
## fork1.py
import os

def child():
	print 'Hello from child', os.getpid()
	os._exit(0)	# else goes back to parent loop

def parent():
	while 1:
		newpid = os.fork()
		if newpid == 0:
			child()
		else:
			print 'Hello from parent', os.getpid(), newpid
		if raw_input()=='q': break

parent()
{%endhighlight%}

The fork() function generates a copy of the calling program, it returns a different value in each copy: zero in the child process, and the process ID of the new child in the parent.

Unfortunately, this won't work on Windows in standard Python today.

The child process functions is also careful to exit explicitly with an os._exit call. If it's not made, the child process would live on after the child function returns. If you delete the exit call and return, you'll likely have to type more than one q to stop, because multiple processes are running in the parent function

{%highlight python%}
## fork-exec.py
import os

parm = 0
while 1:
	parm = parm+1
	pid = os.fork()
	if pid == 0:
		os.execlp('python', 'python', 'child.py', str(parm))
		assert False, 'error starting program'
	else:
		print 'Child is', pid
		if raw_input() == 'q': break


## child.py
import os, sys
print 'Hello from child', os.getpid(), sys.argv[1]
{%endhighlight%}

The combination of os.fork and os.execlp means start a new process and run a new program in that process--in other words, lauch a new program in parallel with original program.

If (os.execlp) successful, the new program begins running and the call to os.execlp itself never returns; If the call does return, an error has occurred.

os.execv(program, commandlinesequence)

os.execl(program, cmdarg1, cmdarg2, ... cmdargN)

> This is the same as os.execv(program, (cmdarg1, cmdarg2,...))

os.execlp

os.execvp

> p means Python will locate the executable's directory using your system search-path settings (i.e., PATH)

os.execle

os.execve

> e means an extra, last argument is a dictionary containing shell environment variables to send to the program.

os.execvpe

os.execlpe

So the above example calls os.execlp, individually passed parameters specify a command line for the program to be run on, and the word *python* maps to an executable file according to the underlying system search-path setting environment variable (PATH). It's as if we were running a command of the form *python child.py 1* in a shell, but with a different command-line argument on the end each time.

## Threads

{%highlight python%}
## thread1.py
import thread

def child(tid):
	print 'Hello from thread', tid

def parent():
	i = 0
	while i:
		i = i+1
		thread.start_new(child, (i,))
		if raw_input() == 'q': break

parent()


## thread-count-mutex.py
import thread, time

def counter(myId, count):
	for i in range(count):
		mutex.acquire()
		#time.sleep(1)
		print '[%s] => %s' % (myId, i)
		mutex.release()

mutex = thread.allocate_lock()
for i in range(10):
	thread.start_new_thread(counter, (i,3))

time.sleep(6)
print 'Main thread exit'


## thread-count-wait1.py
import thread

def counter(myId, count):
	for i in range(count):
		stdoutmutex.acquire()
		print '[%s] => %s' % (myId, i)
		stdoutmutex.release()
	exitmutexes[myId].acquire()	#signal main thread

stdoutmutex = thread.allocate_lock()
exitmutexes = []
for i in range(10):
	exitmutexes.append(thread.allocate_lock())
	thread.start_new(counter, (i, 100))

for mutex in exitmutexes:
	while not mutex.locked(): pass
print 'Main thread exiting.'


## thread-classes.py

import thread

class mythread(threading.Thread):
	def __init__(self, myId, count):
		self.myId = myId
		self.count = count
		threading.Thread.__init__(self)
	
	def run(self):
		for i in range(self.count):
			stdoutmutex.acquire()
			print '[%s] => %s' % (self.myId, i)
			stdoutmutex.release()

stdoutmutex = threading.Lock()	# same as thread.allocate_lock()
threads = []
for i in range(10):
	thread = mythread(i, 100)
	thread.start()
	threads.append(thread)

for thread in threads:
	thread.join()	#wait for thread exits
print 'Main thread exiting'
{%endhighlight%}

The Thread class can also be used to start a simple function without subclassing, though this call form is not noticeably simpler than the basic thread module. For example, the following four code snippets spawn the same sort of thread:

{%highlight python%}
# subclass with state
class mythread(threading.Thread):
	def __init__(self, myId, count):
		self.i = i
		threading.Thread.__init__(self)
	
	def run(self):
		consumer(self.i)

mythread.start()

# pass action in
thread = threading.Thread(target=(lambda: consumer(i)))
thread.start()

# same but no lambda wrapper for state
threading.Thread(target=consumer, args=(i,)).start()

# basic thread module
thread.start_new_thread(consumer, (i,))
{%endhighlight%}

### The Queue Module

{%highlight python%}
## xd5 ueuetest.py

# the queue object is automatically controlled with thread lock acquire and release calls, such that only one thread can modify the queue at any given point in time.

numconsumers = 2
numproducers = 4
nummessages = 4

import thread,Queue,time
safeprint = thread.allocate_lock()
dataQueue = Queue.Queue()

def producer(idnum):
	for msgnum in range(nummessages):
		time.sleep(idnum)
		dataQueue.put('producer %d:%d' % (idnum, msgnum))

def consumer(idnum):
	while 1:
		time.sleep(0.1)
		try:
			data = dataQueue.get(block=False)
		except Queue.Empty:
			pass
		else:
			safeprint.acquire()
			print 'consmer', idnum, 'got =>',data
			safeprint.release()

if __name__ = '__main__':
	for i in range(numconsumers):
		thread.start_new_thread(consumer, (i,))
	for i in range(numproducers):
		thread.start_new_thread(producor, (i,))
	time.sleep(((numproducers-1)* nummessages) + 1)

{%endhighlight%}

### GUIs and Threads

In the context of a GUI, any operation that can block or take a long time to complete must be spawned off in a thread so that the GUI (the main thread) remains active.

The main thread handles all GUI updates and runs a timer-based loop that wakes up periodically to check for new data on the queue to be displayed on screen.

The child threads don't do anything GUI related. They just produce data and put it on the queue be be picked up by the main thread

## Program Exits

{%highlight python%}
>>> sys.exit(N)	# else exits on end of script, with status N

## testexit_sys.py

def later():
	import sys
	print 'Bye sys world'
	sys.exit(42)
	print 'Never reached'

if __name__ == '__main__': later()

>>> from testexit_sys import later
>>> try:
	later()
    except SystemExit:
    	print 'Ignored...'

Bye sys world
Ignored...
>>> from testexit_sys import later
>>> try:
	later()
    finally:
    	print 'Cleanup'

Bye sys world
Cleanup

>>> python testexit_sys.py
Bye sys world
>>> echo $status
42

>>> import os
>>> pipe = os.popen('python testexit_sys.py')
>>> pipe.read()
'Bye sys world\012'
>>> stat = pipe.close()
>>> stat
10752
>>> hex(stat)
'0x2a00'
>>> stat >> 8
42	# 0x2a = 00101010 = 42 

## testexit_os.py

def outahere():
	import os
	print 'Bye os world'
	os._exit(99)	#Unlike os.exit, os_exit is immune to both try/except and try/finally interception
	print 'Never reached'

if __name__ == '__main__': outahere()

>>> from testexit_os import outahere
>>> try:
	outahere()
    except:
    	print 'Ignored'

Bye os world

>>> from testexit_os import outahere
>>> try:
	outahere()
    finally:
    	print 'Cleanup'

Bye os world

>>> python testexit_os.py
Bye os world
>>> echo $status
99
{%endhighlight%}

## Interprocess Communication

### Pipes
{%highlight python%}
## pipe1.py

import os,time

def child(pipeout):
	zzz = 0
	while 1:
		time.sleep(zzz)
		os.write(pipeout, 'Spam %03d' % zzz)
		zzz = (zzz+1)%5

def parent():
	pipein, pipeout = os.pipe()
	if os.fork() == 0:
		child(pipeout)
	else:
		while 1:
			line = os.read(pipein, 32)
			print 'Parent %d got "%s" at %s ' % (os.getpid(), line, time.time())

parent()

>>> python pipe1.py
Parent 6583 got "Spam 000" at 1424657721.27 
Parent 6583 got "Spam 001" at 1424657722.28 
Parent 6583 got "Spam 002" at 1424657724.28 
Parent 6583 got "Spam 003" at 1424657727.28 
Parent 6583 got "Spam 004Spam 000" at 1424657731.28 
Parent 6583 got "Spam 001" at 1424657732.29 
Parent 6583 got "Spam 002" at 1424657734.29 
Parent 6583 got "Spam 003" at 1424657737.29 
Parent 6583 got "Spam 004Spam 000" at 1424657741.29 
Parent 6583 got "Spam 001" at 1424657742.3 
{%endhighlight%}

When child's delay counter hits 004, the parent ends up reading two messages from the pipe at once; the child wrote two distinct messages, but they were close enough in time to be fetched as a single unit by the parent. To distinguish messages better, we can mandate a separator character in the pipe. An end-of-line makes this easy, because we can wrap the pipe descriptor in a file object with os.fdopen and rely on the file's object's readline method to scan up through the next \\n separator in the pipe.

{%highlight python%}
## pipe2.py

import os,time

def child(pipeout):
	zzz = 0
	while 1:
		time.sleep(zzz)
		os.write(pipeout, 'Spam %03d' % zzz)
		zzz = (zzz+1)%5

def parent():
	pipein, pipeout = os.pipe()
	if os.fork() == 0:
		os.close(pipein)
		child(pipeout)
	else:
		os.close(pipeout)
		pipein = os.fdopen(pipein)
		while 1:
			line = pipein.readline()[:-1]
			print 'Parent %d got "%s" at %s ' % (os.getpid(), line, time.time())

parent()
{%endhighlight%}

## Other Ways to Start Programs

{%highlight python%}
## spawnv.py
import os, sys

for i in range(10):
	if sys.platform[:3] == 'win':
		pypath = sys.executable
		os.spawnv(os.P_NOWAIT, pypath, ('python', 'child.py', str(i)))
	else:
		pid = os.fork()
		if pid != 0:
			print 'Process %d spawned' % pid
		else:
			os.execlp('python', 'python', 'child.py', str(i))

print 'Main process exiting.'

#parameters of spawnv:

#os.P_NOWAIT and os.P_NOWAITTO:
## The spawn function will return as soon as the new process has been created, with the process ID as the return value.
#os.P_WAIT
## The spawn function will not return until the new process has run to completion and will return the exit code of the run is successful or '-signal' if a signal kills the process
#os.P_DETACH and os.P_OVERLAY
## P_DETACH is similar to P_NOWAIT, but the new process is detached from the comsole of the calling process. If P_OVERLAY is used, the current program will be replaced (much like os.exec)

{%endhighlight%}

# Chapter 6 System Example: Utilities

{%highlight python%}
## split.py

#!/usr/bin/python
import sys, os
kilobytes = 1024
megabytes = kilobytes*1000
chunksize = int(1.4*megabytes)

def split(fromfile, todir, chunksize=chunksize):
	if not os.path.exists(todir):
		os.mkdir(todir)
	else:
		for fname in os.listdir(todir):
			os.remove(os.path.join(todir, fname))
	partnum = 0
	input = open(fromfile, 'rb')
	while 1:
		chunk = input.read(chunksize)
		if not chunk: break
		partnum = partnum+1
		filename = os.path.join(todir, ('path%04d' % partnum))
		fileobj = open(filename, 'wb')
		fileobj.write(chunk)
		fileobj.close()
	input.close()
	assert partnum <= 9999
	return partnum

if __name__ == '__main__':
	if len(sys.argv) == 2 and sys.argv[1]=='-help':
		print 'Use: split.py [file-to-split target-dir [chunksize]]'
	else:
		if len(sys.argv) < 3:
			interactive = 1
			fromfile = raw_input('File to be split? ')
			todir = raw_input('Directory to store part files? ')
		else:
			interactive = 0
			fromfile, todir = sys.argv[1:3]
			if len(sys.argv) == 4: chunksize = int(sys.argv[3])
		absfrom, absto = map(os.path.abspath, [fromfile, todir])
		print 'Splitting', absfrom, 'to', absto, 'by', chunksize
		
		try:
			parts = split(fromfile, todir, chunksize)
		except:
			print 'Error during split:'
			print sys.exc_info()[0], sys.exc_info()[1]
		else:
			print 'Split finished:', parts, 'parts are in', absto
		if interactive:	raw_input('Press Enter key') 


## join.py
#!/usr/bin/python

import os, sys
readsize = 1024

def join(fromdir, tofile):
	output = open(tofile, 'wb')
	parts = os.listdir(fromdir)
	parts.sort()
	for filename in parts:
		filepath = os.path.join(fromdir, filename)
		fileobj = open(filepath, 'rb')
		while 1:
			filebytes = fileobj.read(readsize)
			if not filebytes: break
			output.write(filebytes)
		fileobj.close()
	output.close()

if __name__ == '__main__':
	if len(sys.argv) == 2 and sys.argv[1]=='-help':
		print 'Use: join.py [form-dir-name to-file-name]'
	else:
		if len(sys.argv) != 3:
			interactive = 1
			fromdir = raw_input('Directory containing part files? ')
			tofile = raw_input('Name of file to be recreated? ')
		else:
			interactive = 0
			fromdir, tofile = sys.argv[1:]
		absfrom, absto = map(os.path.abspath, [fromdir, tofile])
		print 'Joining', absfrom, 'to make', absto

		try:
			join(fromdir, tofile)
		except:
			print 'Error joining files:'
			print sys.exc_info()[0], sys.exc_info()[1]
		else:
			print 'Join complete: see', absto
		if interactive: raw_input('Press Enter Key') 
{%endhighlight%}

## sort filenames

{%highlight python%}
>>> list = ['xx8', 'xx10', 'xx6', 'xx9', 'xx11', 'xx111']
>>> list.sort()
['xx10', 'xx11', 'xx111', 'xx6', 'xx8', 'xx9']
>>> list.sort(lambda x,y: cmp(int(x[2:]), int(y[2:])))
['xx6', 'xx8', 'xx9', 'xx10', 'xx11', 'xx111']
{%endhighlight%}

## A Regression Test Script

{%highlight python%}
## regtest.py

#!/usr/bin/python
import os, sys, time
from glob import glob

print 'RegTest start.'
print 'user:', os.environ['USER']
print 'path:', os.getcwd()
print 'time:', time.asctime(), '\n'
program = sys.argv[1]
testdir = sys.argv[2]

for test in glob(testdir + '/*.in'):
	if not os.path.exists('%s.out' % test):
		os.system('%s < %s > %s.out 2>&1' % (program, test, test)) 
		print 'GENERATED:', test
	else:
		os.rename(test + '.out', test+'.out.bkp')
		os.system('%s < %s > %s.out 2>&1' % (program, test, test))
		os.system('diff %s.out %s.out.bkp > %s.diffs', % ((test,)*3))
		if os.path.getsize(test+'.diffs') == 0:
			print 'PASSED:', test
			os.remove(test+'.diffs')
		else:
			print 'FAILED:', test, '(see %s.diffs)' % test

print 'RegTest done:', time.asctime()
{%endhighlight%}

The *PyUnit* (a.k.a. unittest) and *doctest* standard library modules provide testing frameworks. 

## Parameters

{%highlight python%}
## LaunchBrowser.py
...
def launchBrowser(Mode='-file', Page='index.html', Site=None, verbose=True):
	...

>>> launchBrowser(Page=r'C:\about-pp.html')
>>> launchBrowser(Mode='-live', Page='index.html', Site='www.python.org')
{%endhighlight%}

## A Portable Media File Player Tool

{%highlight python%}
>>> import webbrowser	# standard library
>>> webbrowser.open_new('file://'+fullfilename)	# or http://...

>>> import mimetypes
>>> mimetypes.guess_type('spam.jpg')
('image/jpeg', None)
>>> mimetypes.guess_type('spam.mp3')
('audio/mpeg', None)
>>> mimetypes.guess_type('spam.mpg')
('video/mpeg', None)
>>> mimetypes.guess_type('spam.xyz')
(None, None)
>>> mimetypes.guess_type('spam.gif.gz')
('image/gif', 'gzip')
>>> mimetypes.guess_extension('audio/basic')
'.au'
{%endhighlight%}

# Chapter 7 System Examples: Directories

## Converting Lines Ends in One File

{%highlight python%}
## fixeoln_one.py

import os
listonly = False	# True=show file to be changed, don't rewrite

def convertEndlines(format, fname):	# convert one file
	if not os.path.isfile(fname):	
		print 'Not a text file', fname
		return

	newlines = []
	changed = 0
	for line in open(fname, 'rb').readlines():
		if format == 'todos':	# todos: \n => \r\n
			if line[-1:] == '\n' and line[-2:-1] != '\r':
				line = line[:-1]+'\r\n'
				changed = 1
		elif: format == 'tounix':	# tounix: \r\n => \n
			if line[-2:] == '\r\n':
				line = line[:-2]+'\n'
				changed = 1
		newlines.append(line)

	if changed:
		try:
			print 'Changing', fname
			if not listonly: open(fname, 'wb').writelines(newlines)
		except IOError, why:
			print 'Error writing to file %s: skipped (%s)' % (fname, why)

if __name__ == '__main__':
	import sys
	errmsg = 'Required arguments missing: ["todos" | "tounix"] filename'
	assert (len(sys.argv)==3 and sys.argv[1] in ['todos', 'tounix']), errmsg
	convertEndlines(sys.argv[1], sys.argv[2])
	print 'Converted', sys.argv[2]
{%endhighlight%}

## Redirect

In more general terms, redirecting sys.stdout to dummy objects as done here is a simple way to turn off outputs (and is the equivalent to the Unix notion of redirecting output to the file /dev/null -- a file that discards everything sent to it).

# Chapter 8 Graphical User Interface

{%highlight python%}
## gui1e.py

from Tkinter import *
Label(text='Hello GUI world').pack(expand=YES, fill=BOTH)
mainloop()

# expand=YES option: 
#	Asks the packer to expand the allocated space for the widget in general into any unclaimed space in the widget's parent
# fill option
#	Can be used to stretch the widget to occupy all of its allocated space

def weird():
	spam = 42
	return (lambda: spam*2)

act = weird()
print act()	# prints 84

def weird():
	tmp = (lambda: spam*2)
	spam = 42	# even though not set till here
	return tmp

act = weird()
print act()	# prints 84

def odd():
	funcs = []
	for c in 'abcdefg':
		funcs.append((lambda: c))
	return funcs

for func in odd():
	print func(),	#print 7 g's, not a,b,c...!

def odd():
	funcs = []
	for c in 'abcdefg':
		funcs.append((lambda c=c: c))
	return funcs

for func in odd():
	print func(),	#OK: now prints a,b,c...


## gui3d.py
from Tkinter import *
class HelloCallable:
	def __init__(self):
		self.msg = 'Hello __call__ world'
	def __call__(self):	#implement __call__ to make the class invokable
		print self.msg
		import sys; sys.exit()

widget = Button(None, text='Hello event world', command=HelloCallable())
widget.pack()
widget.mainloop()

#>>> python gui3d.py
#Hello __call__ world

# Binding Events
## gui3e.py
from Tkinter import *

def hello(event):
	print 'Press twice to exit'

def quit(event):
	print 'Hello, I must be going...'
	import sys; sys.exit()

widget = Button(None, text='Hello event world')
widget.pack()
widget.bind('<Button-1>', hello)	# bind left mouse clicks
widget.bind('<Double-1>', hello)	# bind double-left clicks
widget.mainloop()

# Using Anchor to Position Instead of Stretch

Button(win, text='Hello', command=greeting).pack(side=LEFT, anchor=N) # anchor=N, NE, NW, S, etc
Label(win, text='Hello container world').pack(side=TOP)
Button(win, text='Quit', command=win.quit).pack(side=RIGHT)

# Reusable GUI Components with Classes

## gui6.py
from Tkinter import *

class Hello(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		self.data = 42
		self.make_widgets()
	def make_widgets(self):
		widget = Button(self, text='Hello frame world', command=self.message)
		widget.pack(side=LEFT)
	def message(self):
		self.data += 1
		print 'Hello frame world %s!' % self.data

if __name__ == '__main__': Hello().mainloop()

## gui7.py
class HelloPackage:	# Standalone Container Classes
	def __init__(self, parent=None):
		self.top = Frame(parent)
		self.top.pack()
		self.data = 0
		self.make_widgets()
	def make_widgets(self):
		Button(self.top, text='Bye', command=self.top.quit).pack(side=LEFT)
		Button(self.top, text='Hye', command=self.message).pack(side=RIGHT)
	def message(self):
		self.data += 1
		print 'Hello number', self.data
		
if __name__ == '__main__': HelloPackage().top.mainloop()
{%endhighlight%}

# Chapter 9 A Tkinter Tour, Part 1

## Configuring Widget Appearance
{%highlight python%}
## config-label.py

from Tkinter import *
root = Tk()	# The Tk widget is roughly like a Toplevel, but it is used to represent the application root window
labelfont = ('times', 20, 'bold')	# family, size, style
widget = Label(root, text='Hello config world')
widget.config(bg='black', fg='yellow')
widget.config(font=labelfont)
widget.config(height=3, width=20)
widget.pack(expand=YES, fill=BOTH)
root.mainloop()

{%endhighlight%}

## Top-Level Windows

{%highlight python%}
## toplevel0.py 

import sys
from Tkinter import *

win1 = Toplevel()
win2 = Toplevel()

Button(win1, text='Spam', command=sys.exit).pack()
Button(win2, text='SPAM', command=sys.exit).pack()

Label(text='Popups').pack()
win1.mainloop()
{%endhighlight%}

## Top-Level Window Protocols

{%highlight python%}
## toplevel2.py 

import sys
from Tkinter import *

root = Tk()

trees = [('The Larch!','light blue'), ('The Pine!', 'light green'), ('The Giant Redwood!', 'red')]

for (tree, color) in trees:
	win = Toplevel(root)
	win.title('Sing...')
	win.protocol('WM_DELETE_WINDOW', lambda:0)	# ignore close event

	msg = Button(win, text=tree, command=win.destroy)	# kills one win
	msg.pack(expand=YES, fill=BOTH)
	msg.config(padx=10, pady=10, bd=10, relief=RAISED)
	msg.config(bg='black', fg=color, font=('times', 30, 'bold italic'))

root.title('Lumberjack demo')
Label(root, text='Main window', width=30).pack()
Button(root, text='Quit All', command=root.quit).pack()	# kills all app
root.mainloop()
{%endhighlight%}

## Standard (Common) Dialogs

{%highlight python%}
## dlg1.py 

from Tkinter import *
from tkMessageBox import *

def callback():
	if askyesno('Verify', 'Do you really want to quit?'):
		showwarning('Yes', 'Quit not yet implemented')
	else:
		showinfo('No', 'Quit has been cancelled')

errmsg = 'Sorry, no Spam allowed!'
Button(text='Quit', command=callback).pack(fill=X)
Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
mainloop()


## dialogTable.py 

from tkFileDialog import askopenfilename
from tkColorChooser import askcolor
from tkMessageBox import *
from tkSimpleDialog import askfloat

demos = {
		'Open': askopenfilename,
		'Color':askcolor,
		'Query':lambda: askquestion('Warning', 'You typed "rm *"\nConfirm?'),
		'Error':lambda: showerror('Error!', "He's dead, Jim"),
		'Input':lambda: askfloat('Entry', 'Enter credit card number')
	}


## demoDlg.py 

from Tkinter import *
from dialogTable import demos

class Demo(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		Label(self, text='Basic Demos').pack()
		for (key, value) in demos.items():
			Button(self, text=key, command=value).pack(side=TOP, fill=BOTH)

if __name__ == '__main__': Demo().mainloop()
{%endhighlight%}

## Modal/Nonmodal Dialog

{%highlight python%}
## dlg-custom.py 

import sys
from Tkinter import *
makemodal = (len(sys.argv) > 1) #if nonmodal, the 'popup' button can be pressed multiple times 

def dialog():
	win = Toplevel()
	Label(win, text='Hard drive reformatted!').pack()
	Button(win, text='OK', command=win.destroy).pack()
	if makemodal:
		win.focus_set()	# take over input focus
		win.grab_set()	# disable other windows while I'm open
		win.wait_window()	# wait here until win destroyed
	print 'dialog exit'

root = Tk()
Button(root, text='popup', command=dialog).pack()
root.mainloop()
{%endhighlight%}

## Binding events

{%highlight python%}
## bind.py 

from Tkinter import *

def showPosEvent(event):
	print 'Widget=%s X=%s Y=%s' % (event.widget, event.x, event.y)

def showAllEvent(event):
	print event
	for attr in dir(event):
		print attr, '=>', getattr(event, attr)

def onKeyPress(event):
	print 'Got Key press:', event.char

def onArrowKey(event):
	print 'Got up arrow key press'

def onReturnKey(event):
	print 'Got return key press'

def onLeftClick(event):
	print 'Got left mouse button click'
	showPosEvent(event)

def onRightClick(event):
	print 'Got right mouse button click'
	showPosEvent(event)

def onLeftDrag(event):
	print 'Got left mouse button drag:'
	showPosEvent(event)

def onDoubleLeftClick(event):
	print 'Got double left mouse click'
	showPosEvent(event)
	tkroot.quit()

tkroot = Tk()
labelfont = ('courier', 20, 'bold')
widget = Label(tkroot, text='Hello bind world')
widget.config(bg='red', font=labelfont, height=5, width=20)
widget.pack(expand=YES, fill=BOTH)

widget.bind('<Button-1>', onLeftClick)
widget.bind('<Button-3>', onRightClick)
widget.bind('<Double-1>', onDoubleLeftClick)
widget.bind('<B1-Motion>', onLeftDrag)

widget.bind('<KeyPress>', onKeyPress)
widget.bind('<Up>', onArrowKey)
widget.bind('<Return>', onReturnKey)
widget.focus()
tkroot.title('Click Me')
tkroot.mainloop()
{%endhighlight%}

## Message and Entry

{%highlight python%}

## message.py 

from Tkinter import *
msg = Message(text="Oh by the way, which one's Pink?")
msg.config(bg='pink', font=('times', 16, 'italic'))
msg.pack()
mainloop()


## entry1.py 

from Tkinter import *

def fetch():
	print 'Input => %s' % ent.get()

root = Tk()
ent = Entry(root)
ent.insert(0, 'Type words here')
ent.pack(side=TOP, fill=X)

ent.focus()
ent.bind('<Return>', (lambda event: fetch()))
btn = Button(root, text='Fetch', command=fetch)
btn.pack(side=LEFT)
root.mainloop()

## entry3.py 
from Tkinter import *

fields = 'Name', 'Job', 'Pay'

def fetch(variables):
	for variable in variables:
		print 'Input => "%s"' % variable.get()

def makeform(root, fields):
	form = Frame(root)
	left = Frame(form)
	rite = Frame(form)
	form.pack(fill=X)
	left.pack(side=LEFT)
	rite.pack(side=RIGHT, expand=YES, fill=X)

	variables = []
	for field in fields:
		lab = Label(left, width=5, text=field)
		ent = Entry(rite)
		lab.pack(side=TOP)
		ent.pack(side=TOP, fill=X)
		var = StringVar()	# track changes to the entry value
		ent.config(textvariable=var)
		var.set('enter here')
		variables.append(var)
	return variables

if __name__ == '__main__':
	root = Tk()
	vars = makeform(root, fields)
	Button(root, text='Fetch', command=(lambda: fetch(vars))).pack(side=LEFT)
	root.bind('<Return>', (lambda event: fetch(vars)))
	root.mainloop()

{%endhighlight%}

## Checkbutton, Radiobutton, Scale
{%highlight python%}

## demoCheck.py
from Tkinter import *
from dialogTable import demos

class Demo(Frame):
	def __init__(self, parent=None, **args):
		Frame.__init__(self, parent, args)
		self.pack()
		self.tools()
		Label(self, text="Check demos").pack()
		self.vars = []
		for key in demos.keys():
			var = IntVar()
			Checkbutton(self, text=key, variable=var, command=demos[key]).pack(side=LEFT)
			self.vars.append(var)

	def report(self):
		for var in self.vars:
			print var.get(),
		print

	def tools(self):
		frm = Frame(self)
		frm.pack(side=RIGHT)
		Button(frm, text='State', command=self.report).pack(fill=X)

if __name__ == '__main__': Demo().mainloop()


## demo-check-manual.py
from Tkinter import *

root = Tk()
states = []
for i in range(10):
	var = IntVar()
	chk = Checkbutton(root, text=str(i), variable=var)
	chk.pack(side=LEFT)
	states.append(var)

root.mainloop()
print map((lambda var: var.get()), states)	# apply lambda function on each element of states


## demo-radio-auto.py
from Tkinter import *

root = Tk()
var = IntVar()
for i in range(10):
	rad = Radiobutton(root, text=str(i), value=i, variable=var)
	rad.pack(side=LEFT)

root.mainloop()
print var.get()


## demoScale.py
from Tkinter import *
from dialogTable import demos

class Demo(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		Label(self, text='Scale Demos').pack()
		self.var = IntVar()
		Scale(self, label='Pick demo number', command=self.onMove, variable=self.var, from_=0, to=len(demos)-1).pack()
		Scale(self, label='Pick demo number', command=self.onMove, variable=self.var, from_=0, to=len(demos)-1, length=200, tickinterval=1, showvalue=YES, orient='horizontal').pack()
		Button(self, text='Run demo', command=self.onRun).pack(side=LEFT)
		Button(self, text='State', command=self.report).pack(side=RIGHT)

	def onMove(self, value):
		print 'in onMove', value
	
	def onRun(self):
		pos = self.var.get()
		print 'You picked', pos
		pick = demos.keys()[pos]
		print demos[pick]()
	
	def report(self):
		print self.var.get()

if __name__ == '__main__':
	print demos.keys()
	Demo().mainloop()
{%endhighlight%}

## Image

{%highlight python%}

## imgButton.py
from Tkinter import *
#from ImageTk import PhotoImage	#use this library to handle jpeg

win = Tk()
#igm = PhotoImage(file='v.jpg')
igm = PhotoImage(file='M_007.gif')
Button(win, image=igm).pack()
win.mainloop()


## imgCanvas2.py
from Tkinter import *

win = Tk()
#igm = PhotoImage(file='v.jpg')
igm = PhotoImage(file='M_007.gif')
can = Canvas(win)
can.pack(fill=BOTH)
can.config(width=igm.width(), height=igm.height())
can.create_image(2,2,image=igm, anchor=NW)
win.mainloop()


## create Image Thumbnails
import os, sys, math
from Tkinter import *
import Image
from ImageTk import PhotoImage

def makeThumbs(imgdir, size=(100,100), subdir='thumbs'):
	thumbdir = os.path.join(imgdir, subdir)
	if not os.path.exists(thumbdir):
		os.mkdir(thumbdir)

	thumbs = []
	for imgfile in os.listdir(imgdir):
		imgpath = os.path.join(thumbdir, imgfile)
		try:
			imgobj = Image.open(imgpath)
			imgobj.thumbnail(size)
			thumbs.append((imgfile, imgobj))
		except:
			print 'Skipping: ', imgpath
		return thumbs

def viewer(imgdir, kind=Toplevel, cols=None):
	win = kind()
	win.title('Viewer: ' + imgdir)
	thumbs = makeThumbs(imgdir)
	if not cols:
		cols = int(math.ceil(math.sqrt(len(thumbs))))

	savephotos = []
	while thumbs:
		thumbsrow, thumbs = thumbs[:cols], thumbs[cols:]
		row = Frame(win)
		row.pack(fill=BOTH)
		for (imgfile, imgobj) in thumbsrow:
			size = max(imgobj.size)
			photo = PhotoImage(imgobj)
			link = Button(row, image=photo)
			#handler = lambda savefile=imgfile: ViewOne(imgdir, savefile)
			#link.config(command=handler, width=size, height=size)
			link.pack(side=LEFT, expand=YES)
			savephotos.append(photo)

	Button(win, text='Quit', command=win.quit, bg='beige').pack(fill=X)
	return win, savephotos

if __name__ == '__main__':
	imgdir=(len(sys.argv) > 1 and sys.argv[1]) or 'images'
	main, save = viewer(imgdir, kind=Tk)
	main.mainloop()
{%endhighlight%}

# Chapter 10 A Tkinter Tour, Part 2

## Top-Level Window Menus
{%highlight python%}
##menu_win.py

from Tkinter import *
from tkMessageBox import *

def notdone():
	showerror('Not implemented', 'Not yet available')

def makemenu(win):
	top = Menu(win)
	win.config(menu=top)

	file = Menu(top)
	file.add_command(label='New...', command=notdone, underline=0)
	file.add_command(label='Open...', command=notdone, underline=0)
	file.add_command(label='Quit', command=win.quit, underline=0)
	top.add_cascade(label='File', menu=file, underline=0)

	edit = Menu(top, tearoff=0)
	edit.add_command(label='Cut', command=notdone, underline=0)
	edit.add_command(label='Paste', command=notdone, underline=0)
	edit.add_separator()
	top.add_cascade(label='Edit', menu=edit, underline=0)

	submenu = Menu(edit, tearoff=0)
	submenu.add_command(label='Spam', command=win.quit, underline=0)
	submenu.add_command(label='Eggs', command=notdone, underline=0)
	edit.add_cascade(label='Stuff', menu=submenu, underline=0)

if __name__ == '__main__':
	root = Tk()
	root.title('menu_win')
	makemenu(root)
	msg = Label(root, text='Window menu basics')
	msg.pack(expand=YES, fill=BOTH)
	msg.config(relief=SUNKEN, width=40, height=7, bg='beige')
	root.mainloop()
{%endhighlight%}

## Frame- and Menubutton-Based Menus
{%highlight python%}
## menu_frm.py

from Tkinter import *
from tkMessageBox import *

def notdone():
	showerror('Not implemented', 'Not yet available')

def makemenu(parent):
	menubar = Frame(parent)
	menubar.pack(side=TOP, fill=X)

	fbutton = Menubutton(menubar, text='File', underline=0)
	fbutton.pack(side=LEFT)
	file = Menu(fbutton)
	file.add_command(label='New...', command=notdone, underline=0)
	file.add_command(label='Open...', command=notdone, underline=0)
	file.add_command(label='Quit', command=parent.quit, underline=0)
	fbutton.config(menu=file)

	ebutton = Menubutton(menubar, text='Edit', underline=0)
	ebutton.pack(side=LEFT)
	edit = Menu(ebutton, tearoff=0)
	edit.add_command(label='Cut', command=notdone, underline=0)
	edit.add_command(label='Paste', command=notdone, underline=0)
	edit.add_separator()
	ebutton.config(menu=edit)

	submenu = Menu(edit, tearoff=0)
	submenu.add_command(label='Spam', command=parent.quit, underline=0)
	submenu.add_command(label='Eggs', command=notdone, underline=0)
	edit.add_cascade(label='Stuff', menu=submenu, underline=0)
	return menubar

if __name__ == '__main__':
	root = Tk()
	root.title('menu_frm')
	makemenu(root)
	msg = Label(root, text='Frame menu basics')
	msg.pack(expand=YES, fill=BOTH)
	msg.config(relief=SUNKEN, width=40, height=7, bg='beige')
	root.mainloop()
{%endhighlight%}

## Optionmenus

{%highlight python%}
## optionmenu.py
from Tkinter import *

root = Tk()
var1 = StringVar()
var2 = StringVar()
opt1 = OptionMenu(root, var1, 'spam', 'eggs', 'toast')
opt2 = OptionMenu(root, var2, 'ham', 'bacon', 'sausage')
opt1.pack(fill=X)
opt2.pack(fill=X)
var1.set('spam')
var2.set('ham')
def state(): print var1.get(), var2.get()
Button(root, command=state, text='state').pack()
root.mainloop()
{%endhighlight%}

## Listboxes and Scrollbars

{%highlight python%}
## scrolledlist.py

from Tkinter import *

class ScrolledList(Frame):
	def __init__(self, options, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.makeWidgets(options)
	def handleList(self, event):
		index = self.listbox.curselection()
		label = self.listbox.get(index)
		self.runCommand(label)
	def makeWidgets(self, options):
		sbar = Scrollbar(self)
		list = Listbox(self, relief=SUNKEN)
		sbar.config(command=list.yview)
		list.config(yscrollcommand=sbar.set)
		sbar.pack(side=RIGHT, fill=Y)
		list.pack(side=LEFT, expand=YES, fill=BOTH)
		pos = 0
		for label in options:
			list.insert(pos, label)
			pos += 1
		#list.config(selectmode=SINGLE, setgrid=1)
		list.bind('<Double-1>', self.handleList)
		self.listbox = list
	def runCommand(self, selection):
		print 'You selected:', selection 

if __name__ == '__main__':
	options = map((lambda x: 'Lumberjack-' + str(x)), range(20))
	#options = [('Lumberjack-%s % x) for x in range(20)]
	ScrolledList(options).mainloop()
{%endhighlight%}

## Text

{%highlight python%}

## scrolledtext.py

from Tkinter import *

class ScrolledText(Frame):
	def __init__(self, parent=None, text='', file=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.makeWidgets()
		self.settext(text, file)
	def makeWidgets(self):
		sbar = Scrollbar(self)
		text = Text(self, relief=SUNKEN)
		sbar.config(command=text.yview)
		text.config(yscrollcommand=sbar.set)
		sbar.pack(side=RIGHT, fill=Y)
		text.pack(side=LEFT, expand=YES, fill=BOTH)
		self.text = text
	def settext(self, text='', file=None):
		if file:
			text = open(file, 'r').read()
		self.text.delete('1.0', END)
		self.text.insert('1.0', text)
		self.text.mark_set(INSERT, '1.0')
		self.text.focus()
	def gettext(self):
		return self.text.get('1.0', END+'-1c')

if __name__ == '__main__':
	root = Tk()
	try:
		st = ScrolledText(file=sys.argv[1])
	except IndexError:
		st = ScrolledText(text='Words\ngo here')
	def show(event): print repr(st.gettext())
	root.bind('<Key-Escape>', show)
	root.mainloop()
{%endhighlight%}

## Adding Text-Editing Operations

{%highlight python%}
## simpleedit.py

from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog import asksaveasfilename
from scrolledtext import ScrolledText

class SimpleEditor(ScrolledText):
	def __init__(self, parent=None, file=None):
		frm = Frame(parent)
		frm.pack(fill=X)
		Button(frm, text='Save', command=self.onSave).pack(side=LEFT)
		Button(frm, text='Cut', command=self.onCut).pack(side=LEFT)
		Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
		Button(frm, text='Find', command=self.onFind).pack(side=LEFT)
		ScrolledText.__init__(self, parent, file=file)
		self.text.config(font=('courier', 9, 'normal'))
	def onSave(self):
		filename = asksaveasfilename()
		if filename:
			alltext = self.gettext()
			open(filename, 'w').write(alltext)
	def onCut(self):
		text = self.text.get(SEL_FIRST, SEL_LAST)
		self.text.delete(SEL_FIRST, SEL_LAST)
		self.clipboard_clear()
		self.clipboard_append(text)
	def onPaste(self):
		try:
			text = self.selection_get(selection='CLIPBOARD')
			self.text.insert(INSERT, text)
		except TclError:
			pass
	def onFind(self):
		target = askstring('SimpleEditor', 'Search String?')
		if target:
			where = self.text.search(target, INSERT, END)
			if where:
				print where
				pastit = where + ('+%dc' % len(target))
				#self.text.tag_remove(SEL, '1.0', END)
				self.text.tag_add(SEL, where, pastit)
				self.text.mark_set(INSERT, pastit)
				self.text.see(INSERT)
				self.text.focus()

if __name__ == '__main__':
	try:
		SimpleEditor(file = sys.argv[1]).mainloop()
	except IndexError:
		SimpleEditor().mainloop()
{%endhighlight%}

## Advanced Text and Tag Operations

{%highlight python%}

## texttags.py

from Tkinter import *
root = Tk()
def hello(event): print 'Got tag event'

text = Text()
text.config(font=('courier', 15, 'normal'))
text.config(width=20, height=12)
text.pack(expand=YES, fill=BOTH)
text.insert(END, 'This is\n\nthe meaning\n\nof life.\n\n')

btn = Button(text, text='Spam', command=lambda: hello(0))
btn.pack()
text.window_create(END, window=btn)
text.insert(END, '\n\n')
img = PhotoImage(file='M_007.gif')
text.image_create(END, image=img)

text.tag_add('demo', '1.5', '1.7')
text.tag_add('demo', '3.0', '3.3')
text.tag_add('demo', '5.3', '5.7')
text.tag_config('demo', background='purple')
text.tag_config('demo', foreground='white')
text.tag_config('demo', font=('times', 16, 'underline'))
text.tag_bind('demo', '<Double-1>', hello)
root.mainloop()
{%endhighlight%}

## Canvas

{%highlight python%}
## canvas1.py

from Tkinter import *

canvas = Canvas(width=300, height=300, bg='white')
canvas.pack(expand=YES, fill=BOTH)

canvas.create_line(100,100, 200,200)
canvas.create_line(100,200, 200,300)
for i in range(1,20,2):
	canvas.create_line(0, i, 50, i)

canvas.create_oval(10, 10, 200, 200, width=2, fill='blue')
canvas.create_arc(200,200,300,100)
canvas.create_rectangle(200,200,300,300,width=5, fill='red')
canvas.create_line(0,300,150,150, width=10, fill='green')

photo = PhotoImage(file='M_007.gif')
canvas.create_image(250,0,image=photo, anchor=NW)

widget = Label(canvas, text='Spam', fg='white', bg='black')
widget.pack()
canvas.create_window(100,100,window=widget)
canvas.create_text(100,280,text='Ham')
mainloop()

{%endhighlight%}

## Scrolling Canvas

{%highlight python%}

## scrolledcanvas.py

from Tkinter import *

class ScrolledCanvas(Frame):
	def __init__(self, parent=None, color='brown'):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		canv = Canvas(self, bg=color, relief=SUNKEN)
		canv.config(width=300, height=200)
		canv.config(scrollregion=(0,0,300,1000))
		canv.config(highlightthickness=0)

		sbar = Scrollbar(self)
		sbar.config(command=canv.yview)
		canv.config(yscrollcommand=sbar.set)
		sbar.pack(side=RIGHT, fill=Y)
		canv.pack(side=LEFT, expand=YES, fill=BOTH)

		for i in range(10):
			canv.create_text(150, 50+(i*100), text='spam'+str(i), fill='beige')
		canv.bind('<Double-1>', self.onDoubleClick)
		self.canvas = canv
	def onDoubleClick(self, event):
		print event.x, event.y
		print self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

if __name__ == '__main__': ScrolledCanvas().mainloop()
{%endhighlight%}

## Canvas Events

{%highlight python%}

## scrolledcanvas.py

from Tkinter import *
trace = 1

class CanvasEventDemo:
	def __init__(self, parent=None):
		canvas = Canvas(width=300, height=300, bg='beige')
		canvas.pack()
		canvas.bind('<ButtonPress-1>', self.onStart)	#mouse click
		canvas.bind('<B1-Motion>', self.onGrow)		#mouse is moved with left button being held down
		canvas.bind('<Double-1>', self.onClear)		#double click
		canvas.bind('<ButtonPress-3>', self.onMove)	#right click
		self.canvas = canvas
		self.drawn = None
		self.kinds = [canvas.create_oval, canvas.create_rectangle]
	def onStart(self, event):
		self.shape = self.kinds[0]
		self.kinds = self.kinds[1:]+self.kinds[:1]
		self.start = event
		self.drawn = None
	def onGrow(self, event):
		canvas = event.widget
		if self.drawn: canvas.delete(self.drawn)
		objectId = self.shape(self.start.x, self.start.y, event.x, event.y)
		if trace: print objectId
		self.drawn = objectId
	def onClear(self, event):
		event.widget.delete('all')
	def onMove(self, event):
		if self.drawn:
			if trace: print self.drawn
			canvas = event.widget
			diffX, diffY = (event.x-self.start.x), (event.y-self.start.y)
			canvas.move(self.drawn, diffX, diffY)
			self.start = event

if __name__ == '__main__': 
	CanvasEventDemo()
	mainloop()
{%endhighlight%}

## Binding events on specific items

{%highlight python%}

## canvas-bind.py 

from Tkinter import *

def onCanvasClick(event):
	print 'Got canvas click', event.x, event.y, event.widget
def onObjectClick(event):
	print 'Got Object click', event.x, event.y, event.widget
	print event.widget.find_closest(event.x, event.y)

root = Tk()
canv = Canvas(root, width=100, height=100)
obj1 = canv.create_text(50, 30, text='Click me one')
obj2 = canv.create_text(50, 70, text='Click me two')

canv.bind('<Double-1>', onCanvasClick)
canv.tag_bind(obj1, '<Double-1>', onObjectClick)
canv.tag_bind(obj2, '<Double-1>', onObjectClick)
canv.pack()
root.mainloop()

{%endhighlight%}

## grid

{%highlight python%}

## grid3.py 

from Tkinter import *
colors = ['red', 'white', 'blue']

def gridbox(root):
	Label(root, text='Grid').grid(columnspan=2)
	r = 1
	for c in colors:
		l = Label(root, text=c, relief=RIDGE, width=25)
		e = Entry(root, bg=c, relief=SUNKEN, width=50)
		l.grid(row=r, column=0, sticky=NSEW)
		e.grid(row=r, column=1, sticky=NSEW)
		root.rowconfigure(r, weight=1)
		r = r+1
	root.columnconfigure(0, weight=1)
	root.columnconfigure(1, weight=1)

def packbox(root):
	Label(root, text='Pack').pack()
	for c in colors:
		f = Frame(root)
		l = Label(f, text=c, relief=RIDGE, width=25)
		e = Entry(f, bg=c, relief=SUNKEN, width=50)
		f.pack(side=TOP, expand=YES, fill=BOTH)
		l.pack(side=LEFT, expand=YES, fill=BOTH)
		e.pack(side=RIGHT, expand=YES, fill=BOTH)

root = Tk()
gridbox(Toplevel(root))
packbox(Toplevel(root))
Button(root, text='Quit', command=root.quit).pack()
mainloop()
{%endhighlight%}

## time.sleep loops

{%highlight python%}

## canvasDraw_tags.py

from Tkinter import *
import canvasDraw, time

class CanvasEventsDemo(canvasDraw.CanvasEventDemo):
	def __init__(self, parent=None):
		canvasDraw.CanvasEventDemo.__init__(self, parent)
		self.canvas.create_text(75,8,text='Press o and r to move shapes')
		self.canvas.master.bind('<KeyPress-o>', self.onMoveOvals)
		self.canvas.master.bind('<KeyPress-r>', self.onMoveRectangles)
		self.kinds = self.create_oval_tagged, self.create_rectangle_tagged
	def create_oval_tagged(self, x1, y1, x2, y2):
		objectId = self.canvas.create_oval(x1, y1, x2, y2)
		self.canvas.itemconfig(objectId, tag='ovals', fill='blue')
		return objectId
	def create_rectangle_tagged(self, x1, y1, x2, y2):
		objectId = self.canvas.create_rectangle(x1, y1, x2, y2)
		self.canvas.itemconfig(objectId, tag='rectangles', fill='red')
		return objectId
	def onMoveOvals(self, event):
		print 'moving ovals'
		self.moveInSquares(tag='ovals')
	def onMoveRectangles(self, event):
		print 'moving rectangles'
		self.moveInSquares(tag='rectangles')
	def moveInSquares(self, tag):
		for i in range(5):
			for (diffx, diffy) in [(+20, 0), (0, +20), (-20, 0), (0, -20)]:
				self.canvas.move(tag, diffx, diffy)
				self.canvas.update()
				time.sleep(0.25)

if __name__ == '__main__':
	CanvasEventsDemo()
	mainloop()
{%endhighlight%}

## widget.after events

{%highlight python%}

## canvasDraw_tags_after

from Tkinter import *
import canvasDraw_tags

class CanvasEventsDemo(canvasDraw_tags.CanvasEventsDemo):
	def moveEm(self, tag, moremoves):
		(diffx, diffy), moremoves = moremoves[0], moremoves[1:]
		self.canvas.move(tag, diffx, diffy)
		if moremoves:
			self.canvas.after(250, self.moveEm, tag, moremoves)
	def moveInSquares(self, tag):
		allmoves = [(+20,0), (0,+20), (-20,0), (0,-20)]*5
		self.moveEm(tag, allmoves)

if __name__ == '__main__':
	CanvasEventsDemo()
	mainloop()
{%endhighlight%}

# Chapter 13 Network Scripting

## Socket Programming

{%highlight python%}

## echo-server.py

from socket import *
myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)	#listen, allow 5 pending connects

while True:
	connection, address = sockobj.accept()
	print 'Server connected by', address
	while True:
		data = connection.recv(1024)	#read next line on client socket
		if not data: break
		connection.send('Echo=>' +data)
	connection.close()

## echo-client.py

import sys
from socket import *
serverHost = 'localhost'
serverPort = 50007

message = ['Hello network world']
if len(sys.argv) > 1:
	serverHost = sys.argv[1]
	if len(sys.argv) > 2:
		serverHost = sys.argv[2:]

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))

for line in message:
	sockobj.send(line)
	data = sockobj.recv(1024)
	print 'Client received:', repr(data)

sockobj.close()
{%endhighlight%}

## Forking Servers

{%highlight python%}

## fork-server.py

import os, time, sys
from socket import *
myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)	#listen, allow 5 pending connects

def now():
	return time.ctime(time.time())

activeChildren = []
def reapChildren():
	while activeChildren:
		pid, stat = os.waitpid(0, os.WNOHANG)	# don't hang if no child exited
		if not pid: break
		activeChildren.remove(pid)

def handleClient(connection):
	time.sleep(5)
	while True:
		data = connection.recv(1024)
		if not data: break
		connection.send('Echo=>%s at %s' % (data, now()))
	connection.close()
	os._exit(0)

def dispatcher():
	while True:
		connection, address = sockobj.accept()
		print 'Server connected by', address
		print 'at', now()
		reapChildren()
		childPid = os.fork()
		if childPid == 0:	# child process
			handleClient(connection)
		else:
			activeChildren.append(childPid)
	
dispatcher()
{%endhighlight%}

## Killing the zombies

{%highlight python%}

## fork-server-signal.py

# Much simpler, we don't need to manually track or reap child process
# More accurate, it leaves no zombies temporarily between client requests

import os, time, sys, signal
from socket import *
myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)	#listen, allow 5 pending connects
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

def now():
	return time.ctime(time.time())

def handleClient(connection):
	time.sleep(5)
	while True:
		data = connection.recv(1024)
		if not data: break
		connection.send('Echo=>%s at %s' % (data, now()))
	connection.close()
	os._exit(0)

def dispatcher():
	while True:
		connection, address = sockobj.accept()
		print 'Server connected by', address
		print 'at', now()
		childPid = os.fork()
		if childPid == 0:	# child process
			handleClient(connection)
	
dispatcher()
{%endhighlight%}

## Threading servers

{%highlight python%}

## fork-server-signal.py

# performance is better than fork
# portable

import os, time, sys, signal
from socket import *
myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)	#listen, allow 5 pending connects

def now():
	return time.ctime(time.time())

def handleClient(connection):
	time.sleep(5)
	while True:
		data = connection.recv(1024)
		if not data: break
		connection.send('Echo=>%s at %s' % (data, now()))
	connection.close()

def dispatcher():
	while True:
		connection, address = sockobj.accept()
		print 'Server connected by', address
		print 'at', now()
		thread.start_new(handleClient, (connection,))
	
dispatcher()
{%endhighlight%}

## Multiplexing Servers with select

With the *select* system call, a single event loop can process clients and accept new ones in parallel. Such servers are sometimes called *asynchronous*

That is, when the sources passed to *select* are sockets, we can be sure that socket calls like *accept*, *recv* and *send* will not block the server when applied to objects returned by *select*

{%highlight python%}

## select-server.py

import time, sys
from select import select
from socket import *

myHost = ''
myPort = 50007
if len(sys.argv) == 3:
	myHost, myPort = sys.argv[1:]
numPortSocks = 2

def now():
	return time.ctime(time.time())

mainsocks, readsocks, writesocks = [], [], []
for i in range(numPortSocks):
	portsock = socket(AF_INET, SOCK_STREAM)
	portsock.bind((myHost, myPort))
	portsock.listen(5)	#listen, allow 5 pending connects
	mainsocks.append(portsock)
	readsocks.append(portsock)
	myPort += 1

print 'select-server loop starting'
while True:
	readables, writeables, exceptions = select(readsocks, writesocks, [])
	for sockobj in readables:
		if sockobj in mainsocks:
			newsock, address = sockobj.accept()
			print 'Connect:', address, id(newsock)
			readsocks.append(newsock)
		else:
			data = sockobj.recv(1024)
			print '\tgot', data, 'on', id(sockobj)
			if not data:
				sockobj.close()
				readsocks.remove(sockobj)
			else:
				sockobj.send('Echo=>%s at %s' % (data, now()))
{%endhighlight%}

## A Simple Python File Server

{%highlight python%}

## getfile.py

import os, time, sys, thread
from socket import *

blksz = 1024
defaultHost = ''
defaultPort = 50007

helptext = """
Usage ...
server=> getfile.py  -mode server		[-port nnn] [-host hhh|localhost]
client=> getfile.py [-mode client] -file fff	[-port nnn] [-host hhh|localhost]
"""

def parsecommandline():
	dict = {}
	args = sys.argv[1:]
	while len(args) >= 2:
		dict[args[0]] = args[1]
		args = args[2:]
	return dict

def client(host, port, filename):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((host, port))
	sock.send(filename+'\n')
	dropdir = os.path.split(filename)[1]
	file = open(dropdir, 'wb')
	while True:
		data = sock.recv(blksz)
		if not data: break
		file.write(data)
	sock.close()
	file.close()
	print 'Client got', filename, 'at', now()

def serverthread(clientsock):
	sockfile = clientsock.makefile('r')
	filename = sockfile.readline()[:-1]
	try:
		file = open(filename, 'rb')
		while True:
			bytes = file.read(blksz)
			if not bytes: break
			sent = clientsock.send(bytes)
			assert sent == len(bytes)
	except:
		print 'Error downloading file on server:', filename
	clientsock.close()
	
def server(host, port):
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.bind((defaultHost, defaultPort))
	serversock.listen(5)	#listen, allow 5 pending connects
	while True:
		clientsock, clientaddr = serversock.accept()
		print 'Server connected by', clientaddr, 'at', now()
		thread.start_new_thread(serverthread, (clientsock,))

def now():
	return time.ctime(time.time())

def main(args):
	host = args.get('-host', defaultHost)
	port = int(args.get('-port', defaultPort))
	if args.get('-mode') == 'server':
		if host=='localhost': host = ''
		server(host, port)
	elif args.get('-file'):
		client(host, port, args['-file'])
	else:
		print helptext

if __name__ == '__main__':
	args = parsecommandline()
	main(args)


## getfilegui-2.py

import getfile
from socket import *
from Tkinter import *
from tkMessageBox import showinfo

def onSubmit():
	getfile.client(content['Server'].get(),
			int(content['Port'].get()),
			content['File'].get())
	showinfo('getfilegui-2', 'Download complete')

box = Tk()
labels = ['Server', 'Port', 'File']
rownum = 0
content = {}
for label in labels:
	Label(box, text=label).grid(column=0, row=rownum)
	entry = Entry(box)
	entry.grid(column=1, row=rownum, sticky=E+W)
	content[label] = entry
	rownum += 1

box.columnconfigure(0, weight=0)
box.columnconfigure(1, weight=1)
Button(text='Submit', command=onSubmit).grid(row=rownum, column=0, columnspan=2)

box.title('getfilegui-2')
box.bind('<Return>', (lambda event: onSubmit()))
mainloop()
{%endhighlight%}

# Chapter 14 Client-Side Scripting

## Fetching Files with ftplib

{%highlight python%}
#!/usr/bin/python

# getone.py

import os, sys
from getpass import getpass 

nonpassive = False
filename = 'lawnlake2-jan-03.jpg'
dirname = '.'
sitename = 'ftp.rmi.net'
userinfo = ('lutz', getpass('Pswd?'))	# use () for anonymous
if len(sys.argv) > 1: filename = sys.argv[1]

print 'Connecting...'
from ftplib import FTP
localfile = open(filename, 'wb')
connection = FTP(sitename)
connection.login(*userinfo)
connection.cwd(dirname)
if nonpassive:
	connection.set_pasv(False)

print 'Downloading...'
connection.retrbinary('RETR '+filename, localfile.write, 1024)
connection.quit()
localfile.close()

{%endhighlight%}

## Using urllib to FTP Files

{%highlight python%}
#!/usr/bin/python

# getone-url.lib

import os, getpass
import urllib

filename = 'lawnlake2-jan-03.jpg'
password = getpass.getpass('Pswd?')
remoteaddr = 'ftp://lutz:%s@ftp.rmi.net/%s;type=i' % (password, filename)
print 'Downloading', remoteaddr

# this works too:
# urllib.urlretrieve(remoteaddr, filename)

remotefile = urllib.urlopen(remoteaddr)
localfile = open(filename, 'wb')
localfile.write(remotefile.read())
localfile.close()
remotefile.close()

{%endhighlight%}

## FTP get and put Utilities

{%highlight python%}

#!/usr/bin/python

# getfile.py

from ftplib import FTP
from os.path import exists

def getfile(file, site, dir, user=(), verbose=True, refetch=False):
	if exists(file) and not refetch:
		if verbose: print file, 'already fetched'
	else:
		if verbose: print 'Downloading' file
		local = open(file, 'wb')
		try:
			remote = FTP(site)
			remote.login(*user)
			remote.cwd(dir)
			#retrbinary: downloads the requested file in binary mode
			#retrlines: downloads the requested file in ASCII text mode
			remote.retrbinary('RETR '+file, local.write, 1024)	
			remote.quit()
		finally:
			local.close()
		if verbose: print 'Download done.'

if __name__ == '__main__':
	from getpass import getpass
	file = 'lawnlake2-jan-03.jpg'
	dir = '.'
	site = 'ftp.rmi.net'
	user = ('lutz', getpass('Pswd?'))
	getfile(file, site, dir, user)


# putfile.py
#!/usr/bin/python

from ftplib 

def putfile(file, site, dir, user=(), verbose=True):
	if verbose: print 'Uploading ', file
	local = open(file, 'rb')
	remote = ftplib.FTP(site)
	remote.login(*user)
	remote.cwd(dir)
	remote.setorbinary('STOR ' + file, local, 1024)
	remote.quit()
	local.close()
	if verbose: print 'Upload done'

if __name__ == '__main__':
	dir = '.'
	site = 'ftp.rmi.net'
	import sys, getpass
	pswd = getpass.getpass('Pswd?')
	putfile(sys.argv[1], site, dir, user=('lutz', pswd))

{%endhighlight%}

## Downloading web sites

{%highlight python%}

#!/bin/env python

import os, sys, ftplib
from getpass import getpass
from mimetypes import guess_type

nonpassive = False
remotesite = 'home.rmi.net'
remotedir = '.'
remoteuser = 'lutz'
remotepass = getpass('Password for %s on %s: ' % (remoteuser, remotesite))
localdir = (len(sys.argv) > 1 and sys.argv[1]) or '.'
cleanall = raw_input('Clean local directory first? ')[:1] in ['y', 'Y']

print 'connecting...'
connection = ftplib.FTP(remotesite)
connection.login(remoteuser, remotepass)
connection.cwd(remotedir)
if nonpassive:
	connection.set_pasv(False)

if cleanall:
	for localname in os.listdir(localdir):
		try:
			print 'deleting local', localname
			os.remove(os.path.join(localdir, localname))
		except:
			print 'cannot delete local', localname

count = 0
remotefiles = connection.nlst()	#nlst() gives files list

for remotename in remotefiles:
	mimetype, encoding = guess_type(remotename)
	mimetype = mimetype or '?/?'
	maintype = mimetype.split('/')[0]

	localpath = os.path.join(localdir, remotename)
	print 'downloading', remotename, 'to', localpath,
	print 'as', maintype, encoding or ''
	if maintype == 'text' and encoding==None:
		localfile = open(localpath, 'w')
		callback = lambda line: localfile.write(line+'\n')
		connection.retrlines('RETR '+remotename, callback)
	else:
		localfile = open(localpath, 'wb')
		connection.retrbinary('RETR '+remotename, localfile.write)
	localfile.close()
	count += 1

connection.quit()
print 'Done:', count, 'files downloaded.'
{%endhighlight%}

## Uploading web sites

{%highlight python%}

#!/bin/env python

import os, sys, ftplib
from getpass import getpass
from mimetypes import guess_type

nonpassive = False
remotesite = 'home.rmi.net'
remotedir = '.'
remoteuser = 'lutz'
remotepass = getpass('Password for %s on %s: ' % (remoteuser, remotesite))
localdir = (len(sys.argv) > 1 and sys.argv[1]) or '.'
cleanall = raw_input('Clean local directory first? ')[:1] in ['y', 'Y']

print 'connecting...'
connection = ftplib.FTP(remotesite)
connection.login(remoteuser, remotepass)
connection.cwd(remotedir)
if nonpassive:
	connection.set_pasv(False)

if cleanall:
	for remotename in connection.nlst():
		try:
			print 'deleting remote', remotename
			connection.delete(remotename)
		except:
			print 'cannot delete remote', remotename

count = 0
localfiles = os.listdir(localdir)

for localname in localfiles:
	mimetype, encoding = guess_type(localname)
	mimetype = mimetype or '?/?'
	maintype = mimetype.split('/')[0]

	localpath = os.path.join(localdir, localname)
	print 'uploading', localpath, 'to', localname,
	print 'as', maintype, encoding or ''
	if maintype == 'text' and encoding==None:
		localfile = open(localpath, 'r')
		connection.storlines('STOR '+localname, localfile)
	else:
		localfile = open(localpath, 'rb')
		connection.storbinary('STOR '+localname, localfile)
	localfile.close()
	count += 1

connection.quit()
print 'Done:', count, 'files uploaded.'
{%endhighlight%}

## POP Mail Reader Script

{%highlight python%}

## mailconfig.py
popservername = 'pop.earthlink.net'
popusername = 'pp3e'

smtpservername = 'smtp.comcast.net'

myaddress = 'pp3e@earthlink.net'
mysignature = '--Mark Lutz (http://www.rmi.net/~lutz)'

smtpuser = None
smtppasswdfile = ''

poppasswdfile = r'c:\temp\pymailgui.txt'
sentmailfile = r'.\sentmail.txt'
savemailfile = r'c:\temp\savemail.txt'

## popmail.py
#!/usr/local/bin/python

import poplib, getpass, sys, mailconfig

mailserver = mailconfig.popservername
mailuser = mailconfig.popusername
mailpasswd = getpass.getpass('Password for %s?' % mailserver)

print 'Connecting...'
server = poplib.POP3(mailserver)
server.user(mailuser)
server.pass_(mailpasswd)

try:
	print server.getwelcome()
	msgCount, msgBytes = server.stat()
	print 'There are ', msgCount, 'mail message in', msgBytes, 'bytes'
	print server.list()
	print '-'*80
	raw_input('[Press Enter key]')

	for i in range(msgCount):
		hdr, message, octets = server.retr(i+1)
		for line in message: print line
		print '-'*80
		if i < msgCount-1:
			raw_input('[Press Enter key]')
finally:
	server.quit()
print 'Bye'
{%endhighlight%}

## SMTP Mail Sender Script

{%highlight python%}

#!/usr/local/bin/python

import smtplib, getpass, sys, mailconfig

mailserver = mailconfig.smtpservername

From = raw_input('From? ').strip()
To = raw_input('To? ').strip()
To = To.split(';')
Subj = raw_input('Subj? ').strip()

date = time.ctime(time.time())
text = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n' % (From, ';'.join(To), date, Subj))

print 'Type message text, end with line=(ctrl + D or Z)'

while 1:
	line = sys.stdin.readline()
	if not line:
		break
	# if line[:4] == 'From':
	#	line = '>'+line
	text = text+line

print 'Connecting...'
server = smtplib.SMTP(mailserver)
failed = server.sendmail(From, To, text)
server.quit()
if failed:
	print 'Failed recipients:', failed
else:
	print 'No errors.'
print 'Bye.'

{%endhighlight%}

## Email time

{%highlight python%}
>>> import time
>>> time.ctime(time.time())
>>> import email.Utils
>>> email.Utils.formatdate()
>>> email.Utils.formatdate(localtime=True)
>>> email.Utils.formatdate(usegmt=True)

{%endhighlight%}

## Basic email Interfaces in Action

{%highlight python%}
>>> from email.MIMEMultipart import MIMEMultipart
>>> from email.MIMEText import MIMEText

>>> top = MIMEMultipart()
>>> top['from'] = 'Art <arthur@camelot.org>'
>>> top['to'] = 'pp3e@earthlink.net'

>>> sub1 = MIMEText('nice red uniforms...\n')
>>> sub2 = MIMEText(open('data.txt').read())
>>> sub2.add_header('Content-Disposition', 'attachment', 'filename='data.txt')
>>> top.attach(sub1)
>>> top.attach(sub2)
>>> text = top.as_string()
>>> print text

>>> from email.Parser import Parser
>>> msg = Parser().parsestr(text)
>>> msg['from']
'Art <arthur@camelot.org>'

>>> for part in msg.walk():
	print part.get_content_type()
	print part.get_payload()
	print

{%endhighlight%}

## NNTP: Accessing Newsgroups

{%highlight python%}

## readnews.py

listonly = 0
showhdrs = ['From', 'Subject', 'Date', 'Newsgroups', 'Lines']
try:
	import sys
	servername, groupname, showcount = sys.argv[1:]
	showcount = int(showcount)
except:
	servername = 'news.rmi.net'
	groupname = 'comp.lang.python'
	showcount = 10

print 'Connecting to' servername, ' for ', groupname
form nntplib import NNTP
connection = NNTP(servername)
(reply, subjects) = connection.group(groupname)
print '%s has %s articles: %s - %s' % (name, count, first, last)

fetchfrom = str(int(last)-(showcount-1))
(reply, subjects) = connection.xhdr('subject', (fetchfrom+'-'+last))

for (id, subj) in subjects:
	print 'Article %s [%s]' % (id, subj)
	if not listonly and raw_input('=> Display?') in ['y', 'Y']:
		reply, num, tid, list = connection.head(id)
		for line in list:
			for prefix in showhdrs:
				if line[:len(prefix)] == prefix:
					print line[:80]; break
			if raw_input('=> Show body?') in ['y', 'Y']:
				reply, num, tid, list = connection.body(id)
				for line in list:
					print line[:80]
	print
print connection.quit()
{%endhighlight%}

## HTTP: Accessing Web Sites

{%highlight python%}

## http-getfile.py

import sys, httplib
showlines = 6
try:
	servername, filename = sys.argv[1:]
except:
	servername, filename = 'starship.python.net', '/index.html'

print servername, filename
server = httplib.HTTP(servername)
server.putrequest('GET', filename)
server.putheader('Accept', 'text/html')
server.endheaders()

errcode, errmsh, replyheader = server.getreply()
if errcode != 200:
	print 'Error sending request', errcode
else:
	file = server.getfile()
	data = file.readlines()
	file.close()
	for line in data[:showlines]: print line,
{%endhighlight%}

## Module urllib Revisited

{%highlight python%}

## http-getfile-urllib1.py

import sys, urllib
showlines = 6
try:
	servername, filename = sys.argv[1:]
except:
	servername, filename = 'starship.python.net', '/index.html'

remoteaddr = 'http://%s/%s' % (servername, filename)
print remoteaddr
remotefile = urllib.urlopen(remoteaddr)
remotedata = remotefile.readlines()
remotefile.close()
for line in remotedata[:showlines]: print line,


## http-getfile-urllib2.py

import sys, os, urllib, urlparse
showlines = 6
try:
	servername, filename = sys.argv[1:3]
except:
	servername, filename = 'starship.python.net', '/index.html'

remoteaddr = 'http://%s/%s' % (servername, filename)
if len(sys.argv) == 4:
	localname = sys.argv[3]
else:
	(scheme, server, path, parms, query, frag) = urlparse.urlparse(remoteaddr)
	localname = os.path.split(path)[1]

print remoteaddr, localname
urllib.urlretrieve(remoteaddr, localname)
remotedata = open(localname).readlines()
for line in remotedata[:showlines]: print line,
{%endhighlight%}
