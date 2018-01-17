import os
import sys
import markdown

if len(sys.argv) != 2:
    print("[ERROR]Too much parameter.")
    exit()
filename = sys.argv[1]
farray = filename.split(".")
fextension = farray[-1]
fname = '.'.join(farray[0:len(farray)-1])
if fextension != "md":
    print("[ERROR]" + filename + " is not a markdown file.")
    exit()
url = "cache/" + filename
if os.path.exists(url) is False:
    print("[ERROR]" + filename + " is not exist.")
    exit()
file = open(url, 'r', encoding='utf-8')
md = file.read()
file.close()
extensions = ['markdown.extensions.tables',
              'markdown.extensions.fenced_code',
              'markdown.extensions.nl2br']
html = markdown.markdown(md, extensions=extensions)
fout = open("data/html/" + fname + ".html", 'w', encoding='utf-8')
fout.write(html)
fout = open("data/markdown/" + fname + ".md", 'w', encoding='utf-8')
fout.write(md)
os.remove(url)
