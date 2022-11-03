#!python3

import enum
import os
DIRECTORY = './testcases'

os.system('rm testcases/*')
os.system('./testcase_extractor.sh')

for filename in os.listdir(DIRECTORY):
    text=''
    with open(os.path.join(DIRECTORY, filename), 'r', encoding='utf8') as file:
        line = file.readline()
        line = line.partition(',')[1:][1].rstrip(').\n').split('],[')
        line[0] = line[0][1:]
        line[-1] = line[-1][:-1]
        temp = [item.split(',') for item in line[:-1]]
        temp.append(line[-1].split('],'))
        line = temp
        line[0], line[1], line[2] = line[1], line[2], line[0]
        

        for i, item in enumerate(line):
            if i == 0 or i ==1:
                for num in item:
                    text += num
                text += '\n'
            elif i == 2:
                item.reverse()
                for x in item:
                    text += x.partition(':')[-1]
                text += '\n'
            else:
                size = len(line[0])
                grid = [(['0'] * size) for i in range(size)]
                
                if (item[0] != ''):
                    for x in item:
                        x = x.replace('@[', ',').replace(']',',').split(',')
                        type = x[0]
                        row = int(x[1]) - 1
                        col = int(x[2]) - 1
                        if (type == 'c'):
                            type = 'S'
                        grid[row][col] = type.upper()
                else:
                    print("No initial cells: "+filename)
                for row in grid:
                    text += ''.join(row)
                    text += '\n'

    with open(os.path.join(DIRECTORY, filename), 'w', encoding='utf8') as file:
        file.write(text)
