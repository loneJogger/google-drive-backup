import os
import configparser
from datetime import datetime
import win32com.client

# write entry to log file
def writeLog(type, body):
    entry = '{} - {}'.format(type, body)
    with open('log.txt', 'a') as f:
        f.write('\n')
        f.write(str(datetime.utcnow()))
        f.write('\n')
        f.write(entry)
        f.write('\n')
    return True

# finds all files at all levels within a directory
def mapDirectory(dir):
    found = []
    for root, directories, files in os.walk(dir, False):
        for name in files:
            entry = {'path': str(root), 'name': str(name)}
            found.append(entry)
    return found

# gets the 'name' and 'date modified' fields for a given file
def getMetadata(path, name):
    tags = ['Name', 'Size', 'Item type', 'Date modified', 'Date created']
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path)
    metadata = dict()
    item = ns.ParseName(name)
    for index, attribute in enumerate(tags):
        value = ns.GetDetailsOf(item, index)
        if value:
            metadata[attribute] = value
    return metadata

# read the last_run time from history and then check to see which files need to be uploaded
def checkHistory(files):
    modified = []
    parser = configparser.ConfigParser()
    last_run = '1/1/1970 12:00 AM'
    if os.path.exists('history.ini'):
        parser.read('history.ini')
        last_run = parser['DEFAULT']['last_run']
    for file in files:
        if convertToDatetime(last_run) <= convertToDatetime(file['Date modified']):
            modified.append(file)
    writeHistory(createWindowsDate(), parser)
    return modified

# update the last_run time in history
def writeHistory(date, parser):
    parser['DEFAULT'] = {
        'last_run' : date
    }
    with open('history.ini', 'w') as f:
        parser.write(f)
    return True

# convert date string to datetime
def convertToDatetime(timeString):
    return datetime.strptime(timeString, '%m/%d/%Y %I:%M %p')

# create a windows date format string from a datetime
def createWindowsDate():
    return datetime.now().strftime('%m/%d/%Y %I:%M %p')

# read config file
def readConfig():
    parser = configparser.ConfigParser()
    if os.path.exists('config.ini'):
        parser.read('config.ini')
        dir_path = parser['DEFAULT']['dir_path']
        return { 'dir_path' : dir_path }
    else:
        parser['DEFAULT'] = {
            'dir_path' : 'NO_PATH',
        }
        with open('config.ini', 'w') as f:
            parser.write(f)
        return False
