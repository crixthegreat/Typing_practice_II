#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/5 10:54:41


import json


data = [(1000, 'crix'), (380, 'crix'), (200, 'jenny'), 
        (230, 'crix'), (170, 'jenny'), 
        (3000, 'crix'), (1500, 'judy'), (700, 'jenny'),
        (80, 'crix'),(99, 'jenny')
        ]

data_normal = data[0:5]
data_hard = data[5:]


with open('highscore.tp', 'w') as _file:
    try:
        json.dump(data, _file)
    except:
        print('write file failed')


with open('highscore.tp') as _file:
    try:
        _data = json.load(_file)
    except:
        print('open file failed')

    data_normal = sorted(_data[0:5])
    data_hard = sorted(_data[5:])

    print (data_normal, '\n', data_hard)
        
