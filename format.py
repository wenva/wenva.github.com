#coding=utf-8
#!/usr/bin/python
# coding=cp936
#
# Copyright (C) 2014 Wenva <lvyexuwenfa100@126.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os,re,datetime

basepath="_posts"
filelist=os.listdir(basepath)


ignorelist = ['\.']

for file in filelist:
    match=False
    for ignore in ignorelist:
        if (re.match(ignore, file)):
            match=True
            break
        if (match==False):
            filename=basepath+'/'+file
            filefd=open(filename, 'rb')
            title=filefd.readline()[0:-1]
            datestring=filefd.readline()[0:-1]
            categories=filefd.readline()[0:-1]
            filefd.close()
            if (title!='---' and datestring!=''):
                title=title[1:].strip(' ')
                try:
                    datetime=datetime.datetime.strptime(datestring, '%Y年%m月%d日')
                except:
                    datetime=datetime.datetime.strptime(datestring, '%B %d, %Y')

                datestring=datetime.strftime('%Y-%m-%d')
                newname=basepath+'/'+datestring+'-'+title+'.md'

                # read and write
                filefd=open(filename, 'r')
                lines=filefd.readlines()
                filefd.close()

                filefd=open(filename, 'w')
                formatstring='---\nlayout: post\ntitle: '+'"'+title+'"\ndate: '+datestring+'\ncomments: false\ncategories: '+categories+'\n---\n'
                filefd.writelines(formatstring)
                filefd.writelines(lines[3:])
                filefd.close()

                # rename
                os.rename(filename, newname)

                print newname
                print formatstring

