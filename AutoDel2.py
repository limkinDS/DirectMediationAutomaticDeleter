from ftplib import FTP
import datetime
import os


#connects to the host server on the default port (21), have to figure out how to precise a new port
ftp = FTP('directmediation.spoonds.com')
#ftp.login('username', 'password')
ftp.login('', '')

#changes the working directory
#ftp.cwd('folder that needs the focus')
ftp.cwd('')


def deleteAllFiles(ftp):
    for n in ftp.nlst():
        if (foldercount(n) > 1):
            try:
                if n not in ('.','..'):
                    print('Working on..'+n)
                    try:
                        #ftp.delete(n)
                        print('Deleted...'+n)
                    except Exception:
                        print(n+' Not deleted, we suspect its a directory, changing to '+n)
                        ftp.cwd(n)
                        deleteAllFiles(ftp)
                        ftp.cwd('..')
                        print('Trying to remove directory ..'+n)
                        #ftp.rmd(n)
                        print('Directory, '+n+' Removed')
            except Exception:
                print( 'Trying to remove directory ..'+n)
                #ftp.rmd(n)
                print('Directory, '+n+' Removed')
            countdelete -= 1

files = ftp.mlsd()
folders = ftp.mlsd()

count = 0
countstart = 0

print('files')
"""for file in files:
    
    today = (str(datetime.date.today()-datetime.timedelta(7)))
    name = file[0]
    timestamp = file[1]['modify']
    time1 = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')
    time2 = str(time1).split()
    time = time2[0]

    if time > today:
        countstart += 1
        print(name)

    countdelete = countstart
        #print(len(ftp.nlst()))
        #for (i = 0; i = file.length-1; i++):
            #ftp.delete(name)"""


print('folders')
def foldercount(files):
    countstart = 0
    for file in files:
        
        today = (str(datetime.date.today()-datetime.timedelta(7)))
        name = file[0]
        timestamp = file[1]['modify']
        time1 = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')
        time2 = str(time1).split()
        time = time2[0]

        if time > today:
            countstart += 1
            print(name)

    return countstart


for folder in folders:

        today = str(datetime.date.today()-datetime.timedelta(7))
        name = folder[0]
        timestamp = folder[1]['modify']
        time1 = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')
        time2 = str(time1).split()
        time = time2[0]
        if time > today:
            deleteAllFiles(ftp)

print('Done deleting all Files and Directories')