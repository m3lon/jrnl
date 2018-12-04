# coding=utf-8
from datetime import datetime
import argparse
import dateparser
from itertools import chain
import re
import sys

config = {
    'journal_file':'/Users/m3lon/jrnl/j.txt',
    'time_format':'%Y-%m-%d %H:%M',
}

def read_file(filename=None):
    filename = filename if filename else config['journal_file']
    journal = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = re.split(' ', line, 2)
            time =  l[0] + ' ' + l[1]
            title,content = parse_entry(l[2])
            journal.append({'time':time, 'title':title, 'content':content})
    journal = sorted(journal, key= lambda t:t['time'])
    return journal

def print_file(journal, num=5):
    for s in journal[len(journal)-num:]:
        entry_format = "{time} {title}:{content}".format_map(s)
        if '@' in  entry_format:
            entry_format =  re.sub('(@\w*)', "\033[32;40m"+"\\1"+"\033[0m", entry_format)
        print(entry_format)

def add_color(string):
    return "\033[32;40m"+string+"\033[0m"


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
    
def parse_tag(journal, tags = []):
    journal_tags = []
    for entry in journal:
        for tag in tags:
            fulltext = entry['title']+':'+entry['content']
            if re.search(tag, fulltext):
                if entry in journal_tags:
                    continue
                journal_tags.append(entry)
    return journal_tags        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    composing = parser.add_argument_group('Composing', 'Will make an entry out of whatever follows as arguments')
    composing.add_argument('-date', dest='date', help='Date, e.g. "yesterday at 5pm"')
    reading = parser.add_argument_group('Reading', 'Specifying either of these parameters will display posts of your journal')
    reading.add_argument('-n', dest='limit', metavar="N", help='Shows the last n entries matching the filter', nargs="?", type=int, const=0)
    reading.add_argument('--tags', dest='tags', help='Show the entrys with specific @tags', nargs='*', const=None)
    args = parser.parse_args()
    # print(args)
    # exit()

    if not args.limit and not args.tags:
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
        journal = read_file()
        
        if args.tags :
            journal = parse_tag(journal, args.tags)
        
        num = args.limit if args.limit < len(journal) else len(journal)
        print_file(journal, num)




 




