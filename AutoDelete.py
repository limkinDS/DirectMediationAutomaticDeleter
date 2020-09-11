import re
from ftplib import FTP
from datetime import datetime as dt
from datetime import timedelta
from FTPWalk import FTPWalk


def ftp_login():
    # connects to the host server on the default port (21), have to figure out how to precise a new port
    ftp_server = FTP('directmediation.spoonds.com')
    ftp_server.login('luis', 'xakga5-Zomgaq-pyqwig')

    return ftp_server


def walk_through_folders(connection, path):
    ftp_walk = FTPWalk(connection)

    check_folder = re.compile('\d{14}')
    list_company = []

    for i in ftp_walk.walk(path):
        if (len(i[1]) > 1) and (len(check_folder.findall(str(i[1]))) > 0):
            company = []
            for folder_with_date in i[1]:
                company.append(i[0]+'/'+folder_with_date)
            list_company.append(company)

    return list_company


def delete_any_folder_older_7_days(tree):

    for companies in tree:
        for company in companies:
            date_pid = company.split('/')[4]
            date = date_pid.split('_')[0]
            timestamp_folder = dt.strptime(date, '%Y%m%d%H%M%S')
            if (dt.now() - timestamp_folder) > timedelta(7):
                print(company)



if __name__ == '__main__':
    ftp_server = ftp_login()
    file_tree = walk_through_folders(ftp_server, '/cronus/viamail')
    delete_any_folder_older_7_days(file_tree)
