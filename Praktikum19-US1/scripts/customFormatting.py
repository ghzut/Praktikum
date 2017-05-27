import uncertainties.unumpy as unp
import numpy as np


        


class floatFormat(object):
    def __init__(self, Number, SI='', format=''):
        self.u=Number
        self.SI = SI
        self.p = format

    def __format__(self, format):
        if(self.p==''):
            temp = (r'{:'+format+r'}').format(float(self.u))
        else:
            temp = (r'{:'+self.p+r'}').format(float(self.u))
        return r'\SI{'+temp+r'}{'+self.SI+r'}'

class unpFormat(object):
    def __init__(self, unpNumber, SI='', format=''):
        self.u=unpNumber
        self.SI = SI
        self.p = format

    def __format__(self, format):
        if(self.p==''):
            e=0
            if(unp.std_devs(self.u)==0):
                e=0
            else:
                e=np.log10(float(unp.std_devs(self.u)))
        
            if(e<0):
                p=-e+0.5
            else:
                p=0
            temp1 = (r'{:0.'+(r'{:1.0f}'.format(float(p)))+r'f}').format(float(unp.nominal_values(self.u)))
            temp2 = (r'\pm{:0.'+(r'{:1.0f}'.format(float(p)))+r'f}').format(float(unp.std_devs(self.u)))
        else:
            temp1 = (r'{:'+self.p+r'}').format(float(unp.nominal_values(self.u)))
            temp2 = (r'\pm{:'+self.p+r'}').format(float(unp.std_devs(self.u)))

        return r'\SI{'+temp1+temp2+r'}{'+self.SI+r'}'
      

class strFormat(object):
    def __init__(self, string):
        self.s=string

    def __format__(self, format):
        return (r'{}').format(self.s)


def convert(data, format1=floatFormat, arguments=[], arguments2=[]):
    convertedData=[]
    i=0
    for x in data:
        if arguments:
            convertedData.append(format1(x,*arguments))
        else:
            if arguments2:
                convertedData.append(format1(x,*arguments2[i]))
            else:
                convertedData.append(format1(x))
        i=i+1
    return convertedData