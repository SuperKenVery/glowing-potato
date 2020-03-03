import win10toast,time,sys,threading,os,convert,datetime,wechatHelper
class classroom:
    c,m,e,p,ch,h,b,g,po,pe='语文 数学 英语 物理 化学 历史 生物 地理 政治 体育'.split(' ')
    teachers={'乔战胜':b,
              '终结者':ch,
              'Jane':g,
              '王文悦':c,
              '曹建民':po,
              'zoe':e,
              '陈坤':p,
              '梁宏':h,
              '方善泽':m,
              '孟祥标':pe
              }
    sr={#subject representatives
        '王语桐':c,
        '林飞':m,'张涛':m,
        '张善':e,'洪锦奕':e,
        }

blacklist=['刘瑞珏','腾讯课堂六星教育python十一群']

class chatHistory:
    def __init__(self,history=[],file=r'..\history.data'):
        self.histories=history
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
 
toaster=win10toast.ToastNotifier()
history=chatHistory()
notify=True

folders=[classroom.teachers[x] for x in classroom.teachers.keys()]
for i in folders:
    if not os.path.isdir(i): os.mkdir(i)

def register():
    @itchat.msg_register(itchat.content.ATTACHMENT,isGroupChat=True)
    def gotGroupAttachment(msg):
        if not '实验' in msg['User']['NickName']:return None
        sender=msg['ActualNickName']
        path=wechatHelper.path
        if notify and (sender not in blacklist) and (group not in blacklist):
            toaster.show_toast('收到%s'%msg['FileName'],'来自%s'%sender,duration=-1)
        if sender in classroom.teachers.keys():
            path=os.path.join(path,classroom.teachers[sender])
        elif sender in classroom.sr.keys():
            path=os.path.join(path,classroom.sr[sender])
        convert.processFile(filename=msg['FileName'],path=path,getter=msg['Text'])
        return None

    @itchat.msg_register(itchat.content.PICTURE,isGroupChat=True)
    def gotGroupPicture(msg):
        n=os.path.join(os.getenv('TEMP'),msg['FileName'])
        sender=msg['ActualNickName']
        group=msg['User']['NickName']
        with open(n,'wb') as f:
            f.write(msg['Text']())
        if notify and (group not in blacklist) and (sender not in blacklist) and (sender in classroom.teachers or sender in classroom.sr):
            os.system(n)
        history.append(msg['User']['NickName'][:3]+'\t'+msg['ActualNickName']+' 发了一张图片\t存储在'+n)

    @itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
    def gotGroupText(msg):
        global lastGroup
        path=wechatHelper.path
        sender=msg['ActualNickName']
        group=msg['User']['NickName']
        if notify and (sender not in blacklist) and (group not in blacklist):
            toaster.show_toast(sender+'\t('+group+')',msg['Text'],duration=-1,threaded=True)
        history.append(group[:3]+'\t'+sender+':'+msg['Text'].replace('\n',' '))
        if sender in classroom.teachers.keys():
            path=os.path.join(path,classroom.teachers[sender])
            with open(os.path.join(path,'chat.txt'),'a') as f:
                f.write('老师:'+'\t'+msg['Text']+'\n')
        elif sender in classroom.sr.keys():
            path=os.path.join(path,classroom.sr[sender])
            with open(os.path.join(path,'chat.txt'),'a') as f:
                f.write('科代表:'+'\t'+msg['Text']+'\n')
        lastGroup=msg['User']['NickName']

    @itchat.msg_register(itchat.content.TEXT,isFriendChat=True)
    def gotFriendText(msg,toaster=toaster):
        sender=msg['User']['NickName'] if 'NickName' in msg['User'].keys() else '我'
        if notify and (sender not in blacklist): toaster.show_toast(sender,msg['Text'],duration=-1,threaded=True)
        history.append(sender+':'+msg['Text'].replace('\n',''))

    @itchat.msg_register(itchat.content.ATTACHMENT,isFriendChat=True)
    def gotSelfAttachment(msg):
        if not 'NickName' in msg['User'].keys():
            toaster.show_toast('Got SELF Attachment',msg['FileName'],duration=-1,threaded=True)
            convert.processFile(msg['FileName'],wechatHelper.path,msg['Text'],always=True)
            return None

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

listenThread=threading.Thread(target=listen)
def start():
    listenThread.start()

if __name__=='__main__':
    print("Please run wechatHelper.py")
