import itchat,pdb,os,zipfile,win10toast,time,threading,sys,pickle
from win32com.client import gencache
class chatHistory:
    def __init__(self,history=[],file=r'..\history.data'):
        self.histories=history
        self.saveAs=file
        self.print=''
        self.printall=''
    def append(self,argv):
        self.histories.append(argv)
        self.print+=argv+'\n'
    def __str__(self):
        self.printall+=self.print
        r=self.print[:]
        self.print=''
        return r
if not os.path.isdir(os.join(os.getcwd(),'grab')): os.mkdir(os.join(os.getcwd(),'grab'))
inFolder='grab\\'
os.chdir(os.path.join(sys.path[0],inFolder))
itchat.loggedIn=False
def listen():
    import logging,pythoncom
    logging.basicConfig(filename=os.devnull,filemode='w')
    pythoncom.CoInitialize()
    def setLoggedIn():
        itchat.loggedIn=True
    def login():
        itchat.auto_login(hotReload=True,
                          enableCmdQR=True,
                          statusStorageDir='..\\itchat.pkl',
                          loginCallback=setLoggedIn,
                          exitCallback=login
                          )
    login()
    itchat.run()
lastGroup=None
toaster=win10toast.ToastNotifier()
history=chatHistory()
notify=True
#TODOs:
##1 save chat history
##2 print history from last viewed
##3 don't wait 15 seconds when converting to pdf. verify if .pdf file exists

def parseFileName(filename):
    splitted=filename.split('.')
    name=''
    for i in splitted[:-1]:
        name+=i+'.'
    name=name[:-1]
    end=splitted[-1]
    return name,end

def processFile(filename,getter=None,always=False):
    if type(filename)==list:
        for f,g in zip(filename,getter):
            processFile(f,g,always)
        return()
    name,end=parseFileName(filename)
    if always==True or (end in ['doc','docx','pdf','zip','ppt','pptx','xls','xlsx']):
        if getter!=None:
            tryTimes=10
            done=False
            for i in range(tryTimes):
                try:
                    with open(filename,'wb') as f:
                        f.write(getter())
                    done=True
                except Exception as e:
                    if tryTimes-i==1:
                        toaster.show_toast('%s下载失败'%filename,'%s\n正在重试……'%str(e))
                    else:
                        toaster.show_toast('%s下载失败'%filename,'%s\n失败次数过多，请重新发送。'%str(e))
                if done==True:break
        if end=='doc' or end=='docx':
            wps=gencache.EnsureDispatch('kwps.Application')
            doc=wps.Documents.Open(os.path.join(os.getcwd(),filename))
            pdf=os.path.join(os.getcwd(),parseFileName(filename)[0]+'.pdf')
            doc.SaveAs(pdf,FileFormat=17)
            doc.Close()
        elif end=='zip':
            manager=zipfile.ZipFile(filename)
            filenames=[i.split('/')[-1] for i in manager.namelist()]
            getters=[lambda file=i,m=manager:m.read(file) for i in manager.namelist()]
            processFile(filenames,getters,always)
        elif end=='pdf' or end=='ppt' or end=='pptx' or end=='xls' or end=='xlsx':
            pass
            

@itchat.msg_register(itchat.content.ATTACHMENT,isGroupChat=True)
def gotAttachment(msg):
    if '实验' in msg['User']['NickName']:
        if notify: toaster.show_toast('收到%s'%msg['FileName'],'正在处理...',duration=-1)
        processFile([msg['FileName']],[msg['Text']])
        return None
    else:
        os.chdir('other')
        processFile([msg['FileName']],[msg['Text']])
        os.chdir('..')
        return None
@itchat.msg_register(itchat.content.PICTURE,isGroupChat=True)
def gotGroupPicture(msg):
    n=os.path.join(os.getenv('TEMP'),msg['FileName'])
    with open(n,'wb') as f:
        f.write(msg['Text']())
    if notify: os.system(n)
    history.append(msg['User']['NickName'][:3]+'\t'+msg['ActualNickName']+' 发了一张图片\t存储在'+n)
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def gotGroupText(msg,toaster=toaster):
    global lastGroup
    sender=msg['ActualNickName']
    if notify: toaster.show_toast(sender+'\t('+msg['User']['NickName']+')',msg['Text'],duration=-1,threaded=True)
    history.append(msg['User']['NickName'][:3]+'\t'+sender+':'+msg['Text'].replace('\n',''))
    lastGroup=msg['User']['NickName']
@itchat.msg_register(itchat.content.TEXT,isFriendChat=True)
def gotFriendText(msg,toaster=toaster):
    sender=msg['User']['NickName'] if 'NickName' in msg['User'].keys() else '我'
    if notify: toaster.show_toast(sender,msg['Text'],duration=-1,threaded=True)
    history.append(sender+':'+msg['Text'].replace('\n',''))
@itchat.msg_register(itchat.content.ATTACHMENT,isFriendChat=True)
def gotAttachment(msg):
    if not 'NickName' in msg['User'].keys():
        toaster.show_toast('Got SELF Attachment',msg['FileName'],duration=-1,threaded=True)
        processFile(msg['FileName'],msg['Text'],always=True)
        return None
        


listenThread=threading.Thread(target=listen)
listenThread.start()
def printLines(l):
    x=''
    for i in l:
        x+=i+'\n'
    x=x[:-1]
    print(x)
def _stopNotify(t=None):
    global notify
    notify=False
    if t:
        def start(st=t):
            time.sleep(int(st)*60)#in minutes
            _startNotify()
        p=threading.Thread(target=start)
        p.start()
def _startNotify():
    global notify
    notify=True
def _idlecls():
    print('\n'*40)
def _exit():
    itchat.logout()
    exit()
def _reconnect():
    itchat.logout()
def _history(history,every):
    if every==False:
        print(history)
    else:
        print(history.printall)
def _timeTable():
    import datetime
    t=datetime.time
    c,m,e,p,ch,b,h,po,g,s="语文 数学 英语 物理 化学 生物 历史 政治 地理 自习".split(' ')
    times=[(t(8,0),t(9,0)),(t(9,20),t(10,20)),(t(10,40),t(11,40)),(t(14,0),t(15,0)),(t(15,20),t(16,20)),(t(16,40),t(17,40))]
    lessons=[
        [p,c,m,g,e,h],
        [po,e,ch,c,b,s],
        [b,m,c,ch,p,po],
        [e,b,c,m,s,s],
        [m,h,e,ch,p,g]
        ]
    now=datetime.datetime.now()
    time,weekday=now.time(),now.weekday()
    if not weekday in [1,2,3,4,5]:
        print("It's weekend today. Enjoy!!")
        return
    print(*lessons[weekday],sep='  ')
    for index,lesson in enumerate(times):
        if lesson[0]<time<lesson[1]:
            print('      '*index+'^~~~')
            break
        elif time<lesson[0]:
            print('      '*index+'\b\b^~')
            break
commands={
    'help': lambda:printLines(commands.keys()),
    'send':lambda filename:itchat.send_file(filename,toUserName='filehelper'),
    'reply':lambda message:itchat.send(message,toUserName=lastGroup),
    'folder':lambda:os.system('start explorer.exe '+os.getcwd()),
    'history':lambda every=False:_history(history,every),
    'cls':lambda:os.system("cls"),
    'mute':_stopNotify,
    'dnd':_stopNotify,#do not disturb
    'ring':_startNotify,
    'unmute':_startNotify,
    'dndoff':_startNotify,
    'idlecls':_idlecls,
    'lastGroup':lambda:print(lastGroup),
    'exit':_exit,
    'reconnect':_reconnect,
    'reboot':_reconnect,
    'debug':pdb.set_trace,
    'process':processFile,
    'table':_timeTable,
    'lessons':_timeTable,
    'time':_timeTable
    }
def parse(cmd):
    x=['']
    inPara=False
    direct=False
    for i in cmd:
        if i in ['"',"'"]:
            inPara=not inPara
            continue
        if inPara:
            x[-1]+=i
        else:
            if i==' ':
                x.append('')
            else:
                x[-1]+=i
    return x
        
            
while itchat.loggedIn==False: time.sleep(0.01)
time.sleep(0.01)
os.system("cls")
while True:
    c=parse(input('>>>'))
    try:
        commands[c[0]](*c[1:])
    except TypeError as e:
        print("Argument Error. %s"%str(e))
    except KeyError:
        print("Command not found: %s"%c[0])
    except Exception as e:
        print("Unknown Error. %s"%str(e))
    except:
        print("Unknown Error. ")
