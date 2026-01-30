class Test1: # what if someone wants 30 gold
    orders=['30 gold']

class Test2: #what if someone wants a mat that doesn't exist
    orders=['3 guns']

class Tests:
    def __init__(self,test):
        if test==1:
            test=Test1()
        elif test==2:
            test=Test2()
        self.orders=test.orders