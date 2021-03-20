from block_condition import *

class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = 0
        self._surround_count = -1 #周边雷的数量
        self._condition = Block_Condition.unclicked #初始设置为未点击
        self.set_value(value)

    def get_x(self):
        return self._x #直接传入
    def set_x(self, x):
        self._x = x #输入
    x = property(fget=get_x, fset=set_x) 

    def get_y(self):
        return self._y
    def set_y(self, y):
        self._y = y
    y = property(fget=get_y, fset=set_y)

    def get_value(self):
        return self._value
    def set_value(self, value):
        if value:
            self._value = 1 #是地雷
        else:
            self._value = 0 #不是雷
    value = property(fget=get_value, fset=set_value)

    def get_surround_count(self): #获取周边雷的数量
        return self._surround_count
    def set_surround_count(self, surround_count):
        self._surround_count = surround_count
    surround_count = property(fget=get_surround_count, fset=set_surround_count)

    def get_condition(self): #方块的状态
        return self._condition
    def set_condition(self, value):
        self._condition = value
    condition = property(fget=get_condition, fset=set_condition)


