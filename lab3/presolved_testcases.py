#!/bin/python3
import os

for i in range(0, 16):
    text = ''
    ans = ''
    with open('./'+str(i)+'out.txt', 'r+') as f:
        ans = f.read()
    with open('./battle_validate/'+str(i)+'.txt', 'r+') as f:
        prefix = ''.join(f.readlines()[:3])
        text = prefix + ans
    with open('./battle_validate_complete/'+str(i)+'.txt', 'w+') as f:
        f.write(text)