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
  
For decoding&encoding resons, i have modified the zipfile module, changing cp* codings to gbk. You can search in Baidu:python zipfile 乱码 and see how people in CSDN solved it. 
For persistent notification and staying in the notification center, i modified the win10toast module. First, pass duration=-1 to trigger an error, and locate the position that win10toast destroys the notification. Then add an if-clause:
  if duration>0:
    #original code
    return
remember to make return IN the if clause! 

ENJOY!
