# coding=utf-8
from datetime import datetime
import argparse
import dateparser
import re
import sys

config = {
    'journal_file':'/Users/m3lon/jrnl/j.txt',
    'time_format':'%Y-%m-%d %H:%M',
}

def read_file(num, filename=None):
    filename = filename if filename else config['journal_file']
    journal = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = re.split(' ', line, 2)
            time =  l[0] + ' ' + l[1]
            title,content = parse_entry(l[2])
            journal.append((time, title.strip(), content.strip()))
        journal = sorted(journal, key= lambda t:t[0])
        for s in journal[len(journal)-num:]:
            entry_format = "{0} {1}:{2}".format(s[0],s[1],s[2])
            print(entry_format)

def write_file(string,date=None,filename=None):
    title,content = parse_entry(string)
    time = parse_time(date)
    filename = filename if filename else config['journal_file']
    entry_format = "{0} {1}:{2}".format(time, title, content)
    with open(filename, 'a') as f:
        f.write(entry_format+'\n')
    print("[compose success!]")
        

# 处理输入的字符串为标题：内容
def parse_entry(string):
    # 这里的异常处理之后可以再改进
    try:
        title,content = re.split(r'[!:?.]', string, 1)
    except:
        title = string
        content = ''
    if(len(title) ==1 and ord(title[0]) == 10):
        print("[info]: Compose error, you can't entry an empty line!")
        exit()
    title = title.rstrip()
    content = content.rstrip('\n')
    return title,content

def parse_time(date=None):
     time = dateparser.parse(date) if date else datetime.now()
     time = time.strftime(config['time_format'])
     return time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    composing = parser.add_argument_group('Composing', 'Will make an entry out of whatever follows as arguments')
    composing.add_argument('-date', dest='date', help='Date, e.g. "yesterday at 5pm"')
    reading = parser.add_argument_group('Reading', 'Specifying either of these parameters will display posts of your journal')
    reading.add_argument('-n', dest='limit', metavar="N", help='Shows the last n entries matching the filter', nargs="?", type=int, const=0)
    args = parser.parse_args()

    if not args.limit:
        # write mode
        journal = []
        print("[Compose Entry; press Ctrl+D to finish writing]")
        for line in sys.stdin: 
            entry = line
        try:
            write_file(entry, args.date)
        except:
            print('[info]: Compose error, you can\'t entry an empty line')
            exit()
    else:
        # read mode
        read_file(args.limit)




 




