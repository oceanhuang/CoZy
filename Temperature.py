class Temperature(object):
    def __init__(self, number, tempType):
        self.startType = tempType
        if tempType == 'K':
            self.KTemp = number
            self.CTemp = number - 273.15
            self.FTemp = 5.0/9.0*(number - 32.0) + 273.15
        elif tempType == 'C':
            self.KTemp = number + 273.15
            self.CTemp = number
            self.FTemp = 9.0/5.0*number + 32.0      
        elif tempType == 'F':
            self.KTemp = 5.0/9.0*(number - 32.0) + 273.15
            self.CTemp = 5.0/9.0*(number -32.0)
            self.FTemp = number

    def getCelsius(self):
        return self.CTemp

    def getFarenheit(self):
        return self.FTemp

    def getKelvin(self):
        return self.KTemp

    def __class__(self):
        return "Temperature"

    def __str__(self):
        if self.startType == 'K':
            return str(self.KTemp) + ' K'
        elif self.startType == 'C':
            return str(self.CTemp) + ' C'
        elif self.startType == 'F':
            return str(self.FTemp) + ' F'

    def __add__(self, other):
        if other.__class__() == "Temperature":
            temp = Temperature(self.CTemp + other.getCelsius(), 'C')
            temp.startType = self.startType
            return temp
        else:
            return NotImplemented

    def __sub__(self, other):
        if other.__class__() == "Temperature":
            temp = Temperature(self.CTemp - other.getCelsius(), 'C')
            temp.startType = self.startType
            return temp
        else:
            return NotImplemented
    def __lt__(self, other):
        if other.__class__() == "Temperature":
            return self.CTemp < other.getCelsius()
        else:
            return NotImplemented
    def __le__(self, other):
        if other.__class__() == "Temperature":
            return self.CTemp <= other.getCelsius()
        else:
            return NotImplemented
    def __eq__(self, other):
        if other.__class__() == "Temperature":
            return self.CTemp == other.getCelsius()
        else:
            return NotImplemented
    def __ne__(self, other):
        if other.__class__() == "Temperature":
            return self.CTemp != other.getCelsius()
        else:
            return NotImplemented
    def __gt__(self, other):
        if other.__class__() == "Temperature":
            return self.CTemp > other.getCelsius()
        else:
            return NotImplemented
    def __ge__(self, other):
        if other.__class__() == "Temperature":
            return self.CTemp >= other.getCelsius()
        else:
            return NotImplemented
