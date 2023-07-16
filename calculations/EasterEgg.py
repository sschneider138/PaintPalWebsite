class FibonacciCalculator:
    def __init__(self, fibNum):
        self.fibNum = fibNum

    def recursiveFunc(self, num):
        if num == 0:
            return num
        elif num == 1 or num == 2:
            return 1
        else:
            return self.recursiveFunc(num-1) + self.recursiveFunc(num-2)
        
    def recursiveFuncStart(self):
        return [self.recursiveFunc(self.fibNum), 'Recursive Method']
    
    def dynamicFib(self):
        storage = [0, 1]

        if self.fibNum == 0:
            return storage[0]
        elif self.fibNum == 1:
            return storage[1]
        else:
            for num in range(1, self.fibNum):
                temp = storage[0] + storage[1]
                storage[0], storage[1] = storage[1], temp
            return [storage[1], 'Dynamic Programming Method']
    