__author__ = 'pitochka'

from startSFM import SFM

__OPTIONS__ = 'sfm'
__INPUTDIR__ = '/home/pitochka/server/Input/test/rabbit'
__OUTPUTFILE__ = '/home/pitochka/server/Output/rabbit.nvm'
__SFMDIR__ = '/home/pitochka/server/vsfm/vsfm/bin'

a = SFM(__OPTIONS__, __INPUTDIR__, __OUTPUTFILE__, __SFMDIR__)
a.start()
