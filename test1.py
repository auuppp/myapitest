#!/usr/bin/env python
#coding=utf-8

import requests
import re
import json
class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
    @classmethod
    def get_no_of_instance(self):
        return self.no_inst
ik1 = Kls()
ik2 = Kls()
print ik1.get_no_of_instance()
print Kls.get_no_of_instance()

IND = 'ON'
class Kls(object):
    def __init__(self, data):
        self.data = data
    @staticmethod
    def checkind():
        return (IND == 'ON')
    def do_reset(self):
        if self.checkind():
            print 'Reset done for:', self.data
    def set_db(self):
        if self.checkind():
            self.db = 'New db connection'
        print 'DB connection made for: ', self.data
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()
Kls.checkind()
ik1.checkind()
iterable={"name":"test1",'password':'123456'}
for key in iterable.keys():print key
for value in iterable.values():print value
for item in iterable.items():print item
for item,value in iterable.items(): print item, value

def print_everything(*args):
    for count, thing in enumerate(args):
        print '{0}. {1}'.format(count, thing)
print_everything('apple', 'banana', 'cabbage')