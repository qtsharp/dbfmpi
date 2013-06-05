#!/usr/bin/env python
#coding=utf-8
import os
import time
import random
import config
import subprocess
from doubanfm import DoubanFM_CLI

class FMPI:
    def __inti__(self):
        pass
    '''从播放队列获取歌曲并播放'''
    def play(self,name_or_url,freq=98.5,rate=44100):
        '''调用外部播放命令'''
#        cmd = "mpg123 -m -C -q -s %s | sudo pifm - %s %s"%(name_or_url,freq,rate)
        cmd1 = "mpg123 -m -C -q -s %s"%name_or_url
        cmd2 = "sudo pifm - %s %s"%(freq,rate)
        print 'press q to play next songs,\npress Ctrl+c to terminate'
        self.p1 = subprocess.Popen(cmd1,shell=True,stdout=subprocess.PIPE)
        self.p2 = subprocess.Popen(cmd2,shell=True,stdin=self.p1.stdout,stdout=subprocess.PIPE)
        self.p1.wait()
#        os.system(cmd)
        return 0

    def control(self,key):
        '''has problem'''
        out,err = self.p1.communicate(key)
        return out

    def fmpi(self):
        '''循环检测'''
        c = raw_input('0登陆 1匿名:')
#       c = "1"
        dbfm = DoubanFM_CLI(c)
        while True:
            dbfm.get_songlist()
            for r in dbfm.songlist:
                os.system("clear")
                print '>>>>%s'%r['title']+"--"+r['artist']
                self.play(r['url'],config.freq,config.rate)
                time.sleep(1)#降低CPU占用率

if __name__=='__main__':
    pi = FMPI()
    pi.fmpi()