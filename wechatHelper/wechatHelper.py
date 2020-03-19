import itchat,os,sys,datetime

os.system("title WeChat Helper")
inFolder='grab\\'
todayFolder=str(datetime.date.today())
path=os.path.join(sys.path[0],inFolder,todayFolder)
if not os.path.isdir(inFolder):
    os.mkdir(inFolder)
if not os.path.isdir(path):
    os.mkdir(path)
os.chdir(path)

if __name__=='__main__':
    import shell,convert,listen

    itchat.loggedIn=False

    listen.itchat=itchat
    listen.shell=shell
    listen.register()
    listen.start()

    convert.toaster=listen.toaster

    shell.notify,shell.itchat,shell.history=listen.notify,itchat,listen.history
    shell.run()
