import sys
import time
import pygame
from pygame.locals import *
from mine_block import *
from Mine import *
import block_condition 
BLOCK_WIDTH = 30 #横向30块
BLOCK_HEIGHT = 20 #纵向20块
SIZE=30 #一个小方块的边长
SCREEN_WIDTH = BLOCK_WIDTH * SIZE # 游戏屏幕的宽
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE # 游戏屏幕的高

ready=0
start=1
win=2
lose=3
game_dict=[ready, start, win, lose]#四个标志用来判断游戏的进行与否
#ready:准备就绪  start:游戏开始  win:胜利  lose:失败

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #设置窗口大小
    pygame.display.set_caption('欢迎来到艾欧尼亚->扫雷') #设置标题

    png0 = pygame.image.load('./number_mine/0.png').convert() #png支持高级别无损耗压缩
    png0 = pygame.transform.smoothscale(png0, (SIZE, SIZE)) #平滑地将曲面缩放到任意大小，使得图片一样大
    png1 = pygame.image.load('./number_mine/1.png').convert()
    png1 = pygame.transform.smoothscale(png1, (SIZE, SIZE))
    png2 = pygame.image.load('./number_mine/2.png').convert()
    png2 = pygame.transform.smoothscale(png2, (SIZE, SIZE))
    png3 = pygame.image.load('./number_mine/3.png').convert()
    png3 = pygame.transform.smoothscale(png3, (SIZE, SIZE))
    png4 = pygame.image.load('./number_mine/4.png').convert()
    png4 = pygame.transform.smoothscale(png4, (SIZE, SIZE))
    png5 = pygame.image.load('./number_mine/5.png').convert()
    png5 = pygame.transform.smoothscale(png5, (SIZE, SIZE))
    png6 = pygame.image.load('./number_mine/6.png').convert()
    png6 = pygame.transform.smoothscale(png6, (SIZE, SIZE))
    png7 = pygame.image.load('./number_mine/7.png').convert()
    png7 = pygame.transform.smoothscale(png7, (SIZE, SIZE))
    png8 = pygame.image.load('./number_mine/8.png').convert()
    png8 = pygame.transform.smoothscale(png8, (SIZE, SIZE))
    png_blank = pygame.image.load('./number_mine/blank.png').convert()
    png_blank = pygame.transform.smoothscale(png_blank, (SIZE, SIZE))
    png_flag = pygame.image.load('./number_mine/flag.png').convert()
    png_flag = pygame.transform.smoothscale(png_flag, (SIZE, SIZE))
    png_ask = pygame.image.load('./number_mine/ask.png').convert()
    png_ask = pygame.transform.smoothscale(png_ask, (SIZE, SIZE))
    png_mine = pygame.image.load('./number_mine/mine.png').convert()
    png_mine = pygame.transform.smoothscale(png_mine, (SIZE, SIZE))
    png_blood = pygame.image.load('./number_mine/blood.png').convert()
    png_blood = pygame.transform.smoothscale(png_blood, (SIZE, SIZE))
    
    face_size = int(SIZE * 1.5)#设置笑脸的大小
    png_face_lose = pygame.image.load('./face/3.png').convert()
    png_face_lose = pygame.transform.smoothscale(png_face_lose, (face_size, face_size))
    png_face_normal = pygame.image.load('./face/1.png').convert()
    png_face_normal = pygame.transform.smoothscale(png_face_normal, (face_size, face_size))
    png_face_win = pygame.image.load('./face/4.png').convert()
    png_face_win = pygame.transform.smoothscale(png_face_win, (face_size, face_size))
    face_pos_x = (SCREEN_WIDTH - face_size) // 2 #笑脸左边在哪个方块
    face_pos_y = (SIZE * 2 - face_size) // 2 #笑脸上边在哪个方块

    png_dict = {0: png0, 1: png1, 2: png2, 3: png3, 4: png4, 5: png5, 6: png6, 7: png7, 8: png8} #依据雷的数目加载相应图片
    bgcolor = (240, 200, 200) #背景色

    block = Mine_Block()
    game_dict1=game_dict[0] #准备就绪
    start_time = None #开始时间
    used_time=0 #声明变量

    while True:
        screen.fill(bgcolor) #填充背景色
        for event in pygame.event.get(): #获取操作
            if event.type == QUIT: #点击右上角的'×'
                sys.exit()
                
            elif event.type == MOUSEBUTTONDOWN:#鼠标点下
                mouse_x, mouse_y = event.pos #获取鼠标位置
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2
                b1, b2, b3 = pygame.mouse.get_pressed()#鼠标点击的位置，左中右
            elif event.type == MOUSEBUTTONUP:
                if y < 0: #点击方块上方
                    if face_pos_x <= mouse_x <= face_pos_x + face_size and face_pos_y <= mouse_y <= face_pos_y + face_size: #判断是否点击笑脸
                        game_dict1=game_dict[0]
                        start_time = time.time()
                        used_time = 0
                        for i in list_mine:
                            for j in i:
                                pos = (j.x * SIZE, (j.y + 2) * SIZE)
                                j.surround_count = -1 #把周边雷的数目回归到原始状态
                                j.condition = Block_Condition.unclicked #所有方块回归为未点击状态
                                screen.blit(png_blank, pos)
                        pygame.display.flip()
                        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), BLOCK_WIDTH * BLOCK_HEIGHT):
                            list_mine[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 0 #把上一轮雷的定义全部清除                        
                        block=Mine_Block() #重新定义雷
                        continue
                    else:
                        continue
                    
                if game_dict1 == game_dict[0]: #状态为准备就绪
                    game_dict1 = game_dict[1] #开始
                    start_time = time.time() #开始计时

                if game_dict1 == game_dict[1]:
                    mine = block.getblock(x, y)
                    if b1 and not b3: #按鼠标左键
                        if mine.condition== Block_Condition.unclicked: #未点击的会点开
                            if not block.open_block(x, y): #中奖了啊，一颗雷
                                game_dict1 = game_dict[3] #游戏状态为失败
                    elif not b1 and b3: #按鼠标右键
                        if mine.condition == Block_Condition.unclicked: #如果未点击，则标记为旗帜(雷)
                            mine.condition = Block_Condition.flag
                        elif mine.condition == Block_Condition.flag: #如果之前的标记是旗帜，则改标记为问号
                            mine.condition = Block_Condition.ask
                        elif mine.condition == Block_Condition.ask: #如果之前的标记是问号，则改为未点击的状态
                            mine.condition = Block_Condition.unclicked

        flag_count = 0 #旗帜为0
        opened_count = 0 #点开的方块为0

        for row in block._block:
            for mine in row:
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if mine.condition == Block_Condition.clicked: #点开了加载图片(数字)，点开的方块加一
                    screen.blit(png_dict[mine.surround_count], pos)
                    opened_count += 1
                elif mine.condition == Block_Condition.bomb: #状态是炸弹
                    screen.blit(png_blood, pos)
                elif mine.condition == Block_Condition.flag: #是旗帜
                    screen.blit(png_flag, pos)
                    flag_count += 1
                elif mine.condition == Block_Condition.ask: #是问号
                    screen.blit(png_ask, pos)
                elif game_dict1 == game_dict[3] and mine.value:
                    screen.blit(png_mine, pos) #失败了显示所有地雷
                elif mine.condition == Block_Condition.unclicked: #是未打开
                    screen.blit(png_blank, pos)
        if event.type == MOUSEMOTION:#用特定的图像显示鼠标的位置
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2
                mine = block.getblock(x, y)
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if y < 0:
                    continue
                else:
                    if mine.condition == Block_Condition.unclicked:
                        screen.blit(png_dict[0],pos)

                    
        font1 = pygame.font.Font(None, SIZE * 2)
        width, height = font1.size('100')
        text1=font1.render('%d'%(MINE_COUNT-flag_count),True,(255,0,0))
        screen.blit(text1,(30,(SIZE*2-height)//2-2)) #打印剩余雷的数量
        
        if game_dict1 == game_dict[1]:
            used_time = int(time.time() - start_time)
        text2=font1.render('%d'%used_time,True,(255,0,0))
        screen.blit(text2,(SCREEN_WIDTH-width-30,(SIZE*2-height)//2-2)) #打印已用时间

        if opened_count + MINE_COUNT == BLOCK_WIDTH * BLOCK_HEIGHT: #点开方块的加上地雷数等于总数
            game_dict1 = game_dict[2] #则视为胜利
        if game_dict1 == game_dict[2]: #游戏的状态为胜利
            screen.blit(png_face_win, (face_pos_x, face_pos_y))
        elif game_dict1 == game_dict[3]: #游戏的状态为失败
            screen.blit(png_face_lose, (face_pos_x, face_pos_y))
        else:
            screen.blit(png_face_normal, (face_pos_x, face_pos_y))

        pygame.display.update()

if __name__ == '__main__':
    main()
