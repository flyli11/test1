import pygame
import sys
import random

pygame.init()

#弹出窗口的设置
screen=pygame.display.set_mode((250,500))

#标题设置
pygame.display.set_caption("俄罗斯方块")

#得分
score=[0]

#帧数统计变量
speed=0

#是否按压下键
press=False
#游戏结束标志
gameover=[]

#方块的创建:每个坐标点作为每一个小元素块的左上角的标定点
all_block=[
	[[0,0],[0,-1],[0,1],[0,2]],#1
	[[0,0],[0,1],[1,1],[1,0]],#田
	[[0,0],[0,-1],[-1,0],[-1,1]],#Z
	[[0,0],[0,1],[-1,-1],[-1,0]],#镜像Z
	[[0,0],[0,1],[1,0],[0,-1]],#T
	[[0,0],[1,0],[-1,0],[1,-1]],#L
	[[0,0],[1,0],[-1,0],[1,1]],#镜像L
]

#随机选择一个方块
select_block=random.choice(all_block)

#设定游戏的场景为22行10列
background=[[0 for column in range(0,10)] for row in range(0,22)]
#print(background)

#设定方块掉落终止行
background[0]=[1 for _ in range(0,10)]
#print(background)

#设置21行第五列为方块初始掉落位置
block_initial_position=[21,5]

#方块掉落函数
def block_down_move():
	y_drop=block_initial_position[0]
	x_move=block_initial_position[1]
	y_drop-=1

	for row,column in select_block:
		row+=y_drop
		column+=x_move

		if background[row][column]==1:#元素块触底
			break

	else:#没有触底
		block_initial_position.clear()
		block_initial_position.extend([y_drop,x_move])
		return

	#方块触底之后将其状态改变
	y_drop,x_move=block_initial_position
	for row,column in select_block:
		background[row+y_drop][column+x_move]=1

	#判断一行是否被占满，是则将其放进列表中
	complete_row=[]
	for row in range(1,21):
		if 0 not in background[row]:
			complete_row.append(row)

	#用pop消除列表的行前，逆序排列
	complete_row.sort(reverse=True)

	#消除一行或多行并补0
	for row in complete_row:
		background.pop(row)
		background.append([0 for _ in range(0,10)])

	#消除几行加几分
	score[0]+=len(complete_row)
	pygame.display.set_caption("得分为:"+str(score[0])+"分")

	#选择新元素块，清除旧元素块
	select_block.clear()
	select_block.extend(list(random.choice(all_block)))

	#重新设定初始位置
	block_initial_position.clear()
	block_initial_position.extend([20,5])
	y_drop,x_move=block_initial_position

	#判断是否是列中的最后一个元素块
	for row,column in select_block:
		row+=y_drop
		column+=x_move
		if background[row][column]:
			gameover.append(1)

#各类方块的绘制
def draw_block():
	y_drop,x_move=block_initial_position
	for row,column in select_block:
		row+=y_drop
		column+=x_move
		#换算坐标
		point=(column*25,500-row*25)
		#绘制方块
		pygame.draw.rect(screen,(255,255,0),(column*25,500-row*25,23,23))

	#给触底的行和列填充颜色
	for row in range(0,20):
		for column in range(0,10):
			bottom=background[row][column]
			if bottom:
				pygame.draw.rect(screen,(139,117,0),(column*25,500-row*25,23,23))

#控制方块左右函数
def move_left_right(n):
	y_drop,x_move=block_initial_position
	x_move+=n
	for row,column in select_block:
		row+=y_drop
		column+=x_move
		#边界判断
		if column < 0 or column > 9 or background[row][column]:
			break
	else:
		block_initial_position.clear()
		block_initial_position.extend([y_drop,x_move])

#控制方块旋转函数
def rotate():
	y_drop,x_move=block_initial_position
	rotate_position=[(-column,row) for row,column in select_block]
	for row,column in rotate_position:
		row+=y_drop
		column+=x_move
		if column < 0 or column > 9 or background[row][column]:
			break
	else:
		select_block.clear()
		select_block.extend(rotate_position)

#维持弹出的窗口
while True:

	screen.fill(color=(0,191,255))#改变窗口背景颜色

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()

		#读取左右按键
		elif event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT:
			move_left_right(-1)
		elif event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT:
			move_left_right(1)
		#读取上建并旋转
		elif event.type==pygame.KEYDOWN and event.key==pygame.K_UP:
			rotate()
		#读取下键并改变press
		elif event.type==pygame.KEYDOWN and event.key==pygame.K_DOWN:
			press=True
		elif event.type==pygame.KEYUP and event.key==pygame.K_DOWN:
			press=False
	if press:
		speed+=5

	if speed>=30:
		block_down_move()
		speed=0
	else:
		speed+=1
	
	if gameover:
		sys.exit()
	draw_block()
	pygame.time.Clock().tick(100)

	#刷新窗口
	pygame.display.update()