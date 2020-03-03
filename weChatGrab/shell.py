import pdb,threading,time,os,convert,listen

def printLines(l):
    x=''
    for i in l:
        x+=i+'\n'
    x=x[:-1]
    print(x)
def _stopNotify(t=None):
    listen.notify=False
    if t:
        def start(st=t):
            time.sleep(int(st)*60)#in minutes
            _startNotify()
        p=threading.Thread(target=start)
        p.start()
def _startNotify():
    listen.notify=True
def _idlecls():
    print('\n'*40)
def _exit():
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
    if not weekday in [0,1,2,3,4]:
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
def nothing():
    pass
def _process(filename):
    folders=filename.split('\\')
    path=''
    for i in folders[:-1]:
        path+=i+'\\'
    convert.processFile(filename,path)
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
    'process':_process,
    'table':_timeTable,
    'lessons':_timeTable,
    'time':_timeTable,
    '':nothing
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
        
def run():            
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


if __name__=='__main__':
    print("Please run wechatHelper.py")
