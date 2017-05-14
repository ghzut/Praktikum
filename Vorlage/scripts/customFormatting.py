import uncertainties.unumpy as unp
import numpy as np

class floatFormat(object):
    def __init__(self, Number, SI='', p=-1):
        self.u=Number
        self.SI = SI
        self.p = p

    def __format__(self, format):
        if(self.p==-1):
            temp = (r'{:'+format+r'}').format(float(self.u))
        else:
            #print((r'{:3.'+(r'{:1.0}'.format(float(self.p)))+r'}'))
            temp = (r'{:3.'+(r'{:1.0f}'.format(float(self.p)))+r'f}').format(float(self.u))
        return r'\SI{'+temp+r'}{'+self.SI+r'}'

class unpFormat(object):
    def __init__(self, unpNumber, SI=''):
        self.u=unpNumber
        self.SI = SI

    def __format__(self, format):
        e=0
        if(unp.std_devs(self.u)==0):
            e=0
        else:
            e=np.log10(float(unp.std_devs(self.u)))
        
        if(e<0):
            p=-e+0.5
        else:
            p=0
        temp1 = (r'{:3.'+(r'{:1.0f}'.format(float(p)))+r'f}').format(float(unp.nominal_values(self.u)))
        temp2 = (r'\pm{:3.'+(r'{:1.0f}'.format(float(p)))+r'f}').format(float(unp.std_devs(self.u)))
        return r'\SI{'+temp1+temp2+r'}{'+self.SI+r'}'
      

class strFormat(object):
    def __init__(self, string):
        self.s=string

    def __format__(self, format):
        return (r'{}').format(self.s)