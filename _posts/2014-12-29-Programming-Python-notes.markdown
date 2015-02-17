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
{%endhighlight%}
