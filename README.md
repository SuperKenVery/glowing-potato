# glowing-potato
网课：抓取微信附件，FTP服务器等

# Dependencies:

python3, wps

python packages:

    itchat,win32com,win10toast,pyftpdlib
  
# Start using:

Go into the 'simplest ftp server.py' and change the ip address as yours. 

If you are linux, change the PDF converting part to using libreoffice:

    os.system('libreoffice --convert-to pdf "'+filename+'"')
  
Go into "dependencies" folder and run "buildDependencies.py" to modify the libraries needed to run this. 
