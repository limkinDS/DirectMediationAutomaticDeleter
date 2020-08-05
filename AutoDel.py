from ftplib import FTP
import datetime
import os
    #host = "directmediation.spoonds.com"
    #port = 22
    #user = "luis"
    #pwd = "xakga5-Zomgaq-pyqwig"

#connects to the host server on the default port (21), have to figure out how to precise a new port
ftp = FTP('directmediation.spoonds.com')
#ftp.login('username', 'password')
ftp.login('luis', 'xakga5-Zomgaq-pyqwig')

#changes the working directory
#ftp.cwd('Focus directory')
ftp.cwd('luis')


files = ftp.mlsd()
folders = ftp.mlsd()

count = 0
countstart = 0

print('files')
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

    countdelete = countstart
        #print(len(ftp.nlst()))
        #for (i = 0; i = file.length-1; i++):
            #ftp.delete(name)


print('folders')
for folder in folders:

        today = str(datetime.date.today()-datetime.timedelta(7))
        name = folder[0]
        timestamp = folder[1]['modify']
        time1 = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')
        time2 = str(time1).split()
        time = time2[0]
        if time > today:
            if (countdelete > 1):
                print(name)
                #ftp.rmd(name)
                countdelete -= 1