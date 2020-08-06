from ftplib import FTP
import datetime
import os


# host = "directmediation.spoonds.com"
# port = 22
# user = "luis"
# pwd = "xakga5-Zomgaq-pyqwig"


def ftp_login():
    # connects to the host server on the default port (21), have to figure out how to precise a new port
    ftp_server = FTP('directmediation.spoonds.com')
    ftp_server.login('luis', 'xakga5-Zomgaq-pyqwig')

    # changes the working directory
    ftp_server.cwd('luis')

    return ftp_server


def folder_count(ftp_server):
    files = ftp_server.mlsd()

    count_start = 0

    print('files')
    for file in files:

        today = (str(datetime.date.today() - datetime.timedelta(7)))
        name = file[0]
        timestamp = file[1]['modify']
        time1 = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')
        time2 = str(time1).split()
        time = time2[0]

        if time > today:
            count_start += 1
            print(name)

        count_delete = count_start
        # print(len(ftp.nlst()))
        # for (i = 0; i = file.length-1; i++):
        # ftp.delete(name)

        return count_delete


def folder_delete(count_delete, ftp_server):
    folders = ftp_server.mlsd()
    print('folders')
    for folder in folders:

        today = str(datetime.date.today() - datetime.timedelta(7))
        name = folder[0]
        timestamp = folder[1]['modify']
        time1 = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')
        time2 = str(time1).split()
        time = time2[0]
        if time > today:
            if count_delete > 1:
                print(name)
                # ftp.rmd(name)
                count_delete -= 1


if __name__ == '__main__':
    ftp_server = ftp_login()
    count_delete = folder_count(ftp_server)
    folder_delete(count_delete, ftp_server)
