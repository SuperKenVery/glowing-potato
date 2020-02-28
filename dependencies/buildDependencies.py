import os
print('''
This file is used to do all the modifies needed to run my program. 
This is your last chance to watch this file's code, for it won't 
tell you anything while running. 
Take this at your own risk!

Ctrl-C to exit.''')
os.system("pause")

oritoast=open(r'c:\users\sagat\appdata\local\programs\python\python38\lib\site-packages\win10toast\__init__.py','w')
orizip=open(r'c:\users\sagat\appdata\local\programs\python\python38\lib\zipfile.py','w')
modtoast=open('__init__.py','r')
modzip=open('zipfile.py','r')

oritoast.write(modtoast.read())
orizip.write(modzip.read())

oritoast.close()
orizip.close()
modtoast.close()
modzip.close()
