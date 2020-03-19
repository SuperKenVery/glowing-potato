from win32com.client import gencache
import zipfile,os,win10toast
toaster=win10toast.ToastNotifier()
working=0
def parseFileName(filename):
    splitted=filename.split('.')
    name=''
    for i in splitted[:-1]:
        name+=i+'.'
    name=name[:-1]
    end=splitted[-1]
    return name,end

def processFile(filename,path,getter=None,always=False):
    if type(filename)==list:
        for f,g in zip(filename,getter):
            processFile(f,path,g,always)
        return
    working+=1
    name,end=parseFileName(filename)
    if always==True or (end in ['doc','docx','pdf','zip','ppt','pptx','xls','xlsx','mp3']):
        if getter!=None:
            tryTimes=10
            done=False
            for i in range(tryTimes):
                try:
                    file=getter()
                    done=True
                except BaseException as e:
                    if tryTimes-i>1:
                        toaster.show_toast('%s下载失败'%filename[:8],'正在重试……')
                    else:
                        toaster.show_toast('%s下载失败'%filename[:8],'失败次数过多，请重新发送。')
                if done==True:break
            with open(os.path.join(path,filename),'wb') as f:
                f.write(file)
        if end=='doc' or end=='docx':
            wps=gencache.EnsureDispatch('kwps.Application')
            doc=wps.Documents.Open(os.path.join(path,filename))
            pdf=os.path.join(path,parseFileName(filename)[0]+'.pdf')
            doc.SaveAs(pdf,FileFormat=17)
            doc.Close()
        elif end=='zip':
            manager=zipfile.ZipFile(os.path.join(path,filename))
            fullnames=manager.namelist()
            filenames=[i.split('/')[-1] for i in fullnames]
            for index,i in enumerate(filenames):
                if i=='':
                    del filenames[i]
                    del fullnames[i]
            getters=[lambda f=i:manager.read(f) for i in fullnames]
            processFile(filenames,path,getters,always)
        elif end=='pdf' or end=='ppt' or end=='pptx' or end=='xls' or end=='xlsx' or end=='mp3':
            pass
    working-=1

if __name__=='__main__':
    print("Please run wechatHelper.py")
    
