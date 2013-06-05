#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, time, thread

import json, urllib, httplib, contextlib, random
from select import select
from Cookie import SimpleCookie
from contextlib import closing 

class PrivateFM(object):
    def __init__ (self, username, password):
        self.dbcl2 = None
        self.login(username, password)
    
    def login(self, username, password):
        data = urllib.urlencode({'form_email':username, 'form_password':password})
        with closing(httplib.HTTPConnection("www.douban.com")) as conn:
            conn.request("POST", "/accounts/login", data, {"Content-Type":"application/x-www-form-urlencoded"})
            cookie = SimpleCookie(conn.getresponse().getheader('Set-Cookie'))
            if not cookie.has_key('dbcl2'):
                print 'login failed'
                thread.exit()
                return 
            dbcl2 = cookie['dbcl2'].value
            if dbcl2 and len(dbcl2) > 0:
                self.dbcl2 = dbcl2
                self.uid = self.dbcl2.split(':')[0]
            self.bid = cookie['bid'].value
  
    def get_params(self, typename=None):
        params = {}
        params['r'] = random.random()
        params['uid'] = self.uid
        params['channel'] = '0' 
        if typename is not None:
            params['type'] = typename
        return params

    def communicate(self, params):
        data = urllib.urlencode(params)
        cookie = 'dbcl2="%s"; bid="%s"' % (self.dbcl2, self.bid)
        header = {"Cookie": cookie}
        with closing(httplib.HTTPConnection("douban.fm")) as conn:
            conn.request('GET', "/j/mine/playlist?"+data, None, header)
            result = conn.getresponse().read()
            return result

    def playlist(self):
        params = self.get_params('n')
        result = self.communicate(params)
        return json.loads(result)['song']
     
    def del_song(self, sid, aid):
        params = self.get_params('b')
        params['sid'] = sid
        params['aid'] = aid
        result = self.communicate(params)
        return json.loads(result)['song']

    def fav_song(self, sid, aid):
        params = self.get_params('r')
        params['sid'] = sid
        params['aid'] = aid
        self.communicate(params)

    def unfav_song(self, sid, aid):
        params = self.get_params('u')
        params['sid'] = sid
        params['aid'] = aid
        self.communicate(params)

class DoubanFM_CLI:
    def __init__(self, channel):
        self.user = None
        self.username = ''
        if channel == '0':
            self.private = True
        else:
            self.private = False
        self.ch = 'http://douban.fm/j/mine/playlist?type=p&sid=&channel='+channel

    def get_songlist(self):
        if self.user:
            self.songlist = self.user.playlist()
        elif self.private:
            self.username = raw_input("请输入豆瓣登录账户：") 
            import getpass
            self.password = getpass.getpass("请输入豆瓣登录密码：") 
            self.user = PrivateFM(self.username, self.password)
            self.songlist = self.user.playlist()
        else:
            self.songlist = json.loads(urllib.urlopen(self.ch).read())['song']



