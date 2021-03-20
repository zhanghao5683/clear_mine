import random
import time
from Mine import *
from block_condition import *
BLOCK_WIDTH=30
BLOCK_HEIGHT=20
MINE_COUNT=99 #地雷数量

list_mine=[[]]
list_mine=[[Mine(i,j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]
def get_around(x, y):
    #返回(x, y)周围一圈的点
        return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1) #range是左闭右开
                for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) ]
class Mine_Block:
    def __init__(self):
        self._block = list_mine

        # 埋下地雷的种子
        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), MINE_COUNT):
            self._block[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1
    def getblock(self, x, y):
        return self._block[y][x]
    def open_block(self, x, y):
        # 真不幸，这是颗地雷
        if self._block[y][x].value:
            self._block[y][x].condition = Block_Condition.bomb
            return False

        self._block[y][x].condition = Block_Condition.clicked #没踩雷

        around = get_around(x, y)

        sum1 = 0
        for i, j in around:
            if self._block[j][i].value:
                sum1 += 1
        self._block[y][x].surround_count = sum1

        if sum1 == 0: #周边无雷，向旁边递归，一点打开一片
            for i, j in around:
                if self._block[j][i].surround_count == -1:
                    self.open_block(i, j)

        return True
