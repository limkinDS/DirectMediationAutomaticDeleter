import logging
import re
from datetime import datetime as dt
from datetime import timedelta
from ftplib import FTP, error_perm
from pathlib import Path

from FTPWalk import FTPWalk

logging.basicConfig(filename='./log/' + str(dt.utcnow().date()) + '.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


def ftp_login():
    # connects to the host server on the default port (21), have to figure out how to precise a new port
    ftp = FTP('directmediation.spoonds.com')
    ftp.login('luis', 'xakga5-Zomgaq-pyqwig')

    return ftp


def tree(ftp_walk, ftp, path: Path, prefix: str = ''):
    # prefix components:
    space = '    '
    branch = '│   '
    # pointers:
    tee = '├── '
    last = '└── '

    root = path + '/'

    contents = list(ftp_walk.listdir(path)[0])
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path
        if is_dir(ftp, path):  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(ftp_walk, ftp, root + path, prefix=prefix + extension)


def is_dir(ftp, path):
    try:
        ftp.cwd(path)
        return False
    except error_perm:
        return True


def walk_through_folders_and_delete(ftp):
    ftp_walk = FTPWalk(ftp)
    path = '/cronus/viamail/'

    check_folder = re.compile('\\d{14}')

    logging.info('###### FTP Directory Tree ######')
    for line in tree(ftp_walk, ftp, path):
        logging.info(line)

    logging.info('###### Deleting Directories ######')
    logging.info('\t• empty directories')
    logging.info('\t• older then 7 days')
    logging.info('\t• not the only directory for the company')
    logging.info('\t• oldest of multiple directories')

    count = 0
    skipped_dir = []

    for i in ftp_walk.walk(path):
        root = i[0]
        files = i[2]

        if check_folder.search(root):
            if len(files) == 0:  # check if any files are in dir
                if folder_date_older_7_days(root):  # check if folder is older then 7 days
                    if check_if_youngest_and_not_only_folder(root):  # youngest and not only folder in root
                        logging.info('Deleting %s', root)
                        ftp.rmd(root)  # delete dir
                        count = count + 1
            else:
                if folder_date_older_7_days(root):  # check if folder is older then 7 days
                    skipped_dir.append(root)

    logging.info("Deleted %s directories", str(count))

    logging.info("###### Non-Deleted Full Directories ######")
    for s_dir in skipped_dir:
        logging.info("Folder with file %s", s_dir)
    logging.info("Skipped %s directories", str(len(skipped_dir)))


def check_if_youngest_and_not_only_folder(root):
    split_path = root.split('/')
    folder_with_timestamp = split_path[4]
    folder_with_date = folder_with_timestamp.split('_')[0]
    datetime_of_folder = dt.strptime(folder_with_date, '%Y%m%d%H%M%S')

    cut_root = root.replace('/' + folder_with_timestamp, '')

    # make a new connection to ftp
    with ftp_login() as ftp:
        ftp_walk = FTPWalk(ftp)
        directories = ftp_walk.listdir(cut_root)[0]

    # Checks if in directory is more then one file
    if len(directories) <= 1:
        return False

    for i in directories:

        dir_with_date = i.split('_')[0]
        datetime_of_dir = dt.strptime(dir_with_date, '%Y%m%d%H%M%S')
        if datetime_of_folder < datetime_of_dir:
            return True

    return False


def folder_date_older_7_days(folder):
    date_pid = folder.split('/')[4]
    date = date_pid.split('_')[0]
    timestamp_folder = dt.strptime(date, '%Y%m%d%H%M%S')
    if (dt.now() - timestamp_folder) > timedelta(7):
        return True
    else:
        return False


def send_log_to_ftp(ftp):
    ftp.cwd('/cronus/viamail logfiles/')

    with open('./log/' + str(dt.utcnow().date()) + '.log', 'rb') as logfile:
        ftp.storbinary('STOR ' + str(dt.utcnow().date()) + '.log', logfile)


if __name__ == '__main__':
    with ftp_login() as ftp_server:
        walk_through_folders_and_delete(ftp_server)
        send_log_to_ftp(ftp_server)
