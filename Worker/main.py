# coding=utf8
__author__ = 'pitochka'

from startSFM import triangulate
from startSFM import convert
from worker import getTask

__INPUTDIR__ = '/home/pitochka/server/Input/test/rabbit'
__OUTPUTFILE__ = '/home/pitochka/server/Output/rabbit.ply'
__SFMDIR__ = '/home/pitochka/server/vsfm/vsfm/bin'

#a = SFM(__INPUTDIR__, __OUTPUTFILE__, __SFMDIR__)
# a.start()
a = getTask() #Главный файл
#a = convert('/home/pitochka/server/Output/rabbit.nvm', '/home/pitochka/server/Output/rabbit.ply')
a()
#b = triangulate('/home/pitochka/server/Output/rabbit.ply', '/home/pitochka/server/Output/rabbit.obj', '/home/pitochka/server/Output/2.mlx')
#b()