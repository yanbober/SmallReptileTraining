#!/usr/bin/python
# -*- coding:utf-8 -*-
 
num = int(raw_input("请输入要分解的正整数："))
 
temp = []
while num!=1:
    for i in range(2,num+1):
        if num%i == 0:
            temp.append(i)
            num /= i
            break
print temp