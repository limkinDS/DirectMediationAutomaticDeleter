from ftplib import FTP
import datetime


# host = "directmediation.spoonds.com"
# port = 22
# user = "luis"
# pwd = "xakga5-Zomgaq-pyqwig"


def ftp_login():
    # connects to the host server on the default port (21), have to figure out how to precise a new port
    ftp_server_login = FTP('directmediation.spoonds.com')
    ftp_server_login.login('luis', 'xakga5-Zomgaq-pyqwig')

    # changes the working directory
    ftp_server_login.cwd('luis')

    return ftp_server_login


def folder_count(ftp_server_count):
    files = ftp_server_count.mlsd()

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

        folder_count_delete = count_start
        # print(len(ftp.nlst()))
        # for (i = 0; i = file.length-1; i++):
        # ftp.delete(name)

        return folder_count_delete


def folder_delete(folder_count_delete, ftp_server_delete):
    folders = ftp_server_delete.mlsd()
    print('folders')
    for folder in folders:

        today = str(datetime.date.today() - datetime.timedelta(7))
        name = folder[0]
        timestamp = folder[1]['modify']
        time1 = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')
        time2 = str(time1).split()
        time = time2[0]
        if time > today:
            if folder_count_delete > 1:
                print(name)
                # ftp.rmd(name)
                folder_count_delete -= 1


if __name__ == '__main__':
    ftp_server = ftp_login()
    count_delete = folder_count(ftp_server)
    folder_delete(count_delete, ftp_server)
