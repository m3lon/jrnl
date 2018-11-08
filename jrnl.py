# coding=utf-8
import datetime
import argparse
import dateparser
import re
import sys

entry = []

parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, help='display n lines from your journal file')
parser.add_argument('-t', type=str, help='entry your time')
args = parser.parse_args()

if not args.n:
    print("[Compose Entry; press Ctrl+D to finish writing]")
    for line in sys.stdin:
        try:
            title,content = re.split(r'[!:?.]', line, 1)
        except:
            pass 
    dt = dateparser.parse(args.t) if args.t else datetime.datetime.now()
    datatime = dt.strftime("%Y-%m-%d %H:%M:%S")
    journal = {'time':datatime, 'title':title, 'content':content}
    journal_txt = "{time} {title} :{content}".format_map(journal)
    print(journal_txt)
    with open('j.txt', 'a') as f:
        f.write(journal_txt+"\n")
    f.close()
    print("[compose success!]")

# def time_parse():
    
if args.n:
    #文本输出
    with open('j.txt', 'r') as f:
        for n in range(args.n):
            data = f.readline()
            if not (len(data) == 1 and ord(data[0]) == 10):
                print(data)
    f.close()






 




