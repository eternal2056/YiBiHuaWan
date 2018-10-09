import win32gui
import win32api
import win32con
from PIL import ImageGrab,Image
import time
from numpy import *
from ctypes import *
import pyautogui
#-------------------------------------第一步-------------------------------
#gdi32 = windll.gdi32
global hwnd
#hwnd 句柄
hwnd = win32gui.FindWindow("TXGuiFoundation","腾讯手游助手【极速傲引擎】")
#若句柄没有值（即没有找到窗口句柄）
if not hwnd:
    print("Window not find!")
else:
    print("句柄：{}".format(hwnd))
#设置窗口最前面
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)
#停顿一秒！
time.sleep(1)
#对角XY
game_rect = win32gui.GetWindowRect(hwnd)
#--------------------------------------------------函数块------------------------------------------------
#图片的颜色分布（字典）
#CPU节能、效率、优化
def yansezidian():
    zidian = {}
    for i in range(549):
        for j in range(704):
            getcolor_1 = list(src_image.getpixel((i,j)))
            zidian[(i,j)] = getcolor_1
    return zidian
#循环算出上边界
def tongji_shang():
    shangbianjie = 300
    shangbianjie_2 = 0
    for i in range(549):
        diyici = True
        for j in range(704):
            getcolor_1 = zidian_waibu.get((i,j))
            if getcolor_1 == heise and diyici == True:
                if shangbianjie > j:
                    shangbianjie = j
                    shangbianjie_2 = i
                diyici = False

    return shangbianjie,shangbianjie_2
#下边界
def tongji_xia():
    xiabianjie = 200
    for i in range(549):
        diyici = True
        for j in range(703,-1,-1):
            getcolor_1 = zidian_waibu.get((i,j))
            if getcolor_1 == heise and diyici == True:
                if xiabianjie < j:
                    xiabianjie = j
                diyici = False
    return xiabianjie
#左边界
def tongji_zuo():
    zuobianjie = 300
    for y in range(704):
        diyici = True
        for x in range(549):
            getcolor_1 = zidian_waibu.get((x,y))
            if getcolor_1 == heise and diyici == True:
                if zuobianjie > x:
                    zuobianjie = x
                diyici = False
    return zuobianjie
#右边界
def tongji_you():
    youbianjie = 400
    for y in range(704):
        diyici = True
        for x in range(548,-1,-1):
            getcolor_1 = zidian_waibu.get((x,y))
            if getcolor_1 == heise and diyici == True:
                if youbianjie < x:
                    youbianjie = x
                diyici = False
    return youbianjie
#从黑色到白色时的黑色点数的个数中最大的是边长
def bianchang():
    bianchang = 0
    zhen_fengxi = 0
    #挑一个没有干扰的实心方块：不是空白，不是起点
    #如果黑色大于60，而且那条竖线下，并没有起点（起点会干扰判断）
    heisechangdu = 0
    max = 0
    for y in range(shangbianjie_waibu,xiabianjie_waibu):
        for x in range(zuobianjie_waibu,youbianjie_waibu):
            if zidian_waibu.get((x,y)) == heise:#如果黑色之后变成RGB不一样的颜色的时候略过那条线
                heisechangdu += 1
                if zidian_waibu.get((x+1,y))[0] != zidian_waibu.get((x+1,y))[1]:
                    heisechangdu = 0
                    break
            #如果没有碰到黑色的话，就算碰到白色也不会计数，也不会退出
            if zidian_waibu.get((x,y)) == baise:
                if heisechangdu != 0:
                    if max < heisechangdu:
                        max = heisechangdu
                    heisechangdu = 0
                    break
                    #最大的黑色长度是边长
        heisechangdu = 0
    return max
#从黑色到白色时开始算白色点数到黑色或其他颜色，并比较出最小值，即缝隙！
def fengxi():
    baisegeshu = 0
    min = 30
    diyici = True
    #第一次碰到黑色前不计数，第二次碰到黑色Break
    for y in range(shangbianjie_waibu,xiabianjie_waibu):
        for x in range(zuobianjie_waibu,youbianjie_waibu):
            if zidian_waibu.get((x,y)) == heise and diyici == True:
                diyici = False
            if zidian_waibu.get((x,y)) == baise and diyici == False:#碰到白色前碰到过黑色时
                baisegeshu += 1
                if zidian_waibu.get((x+1,y)) != baise:
                    #print(baisegeshu, end=" ")
                    if min > baisegeshu:
                        min = baisegeshu
                    baisegeshu = 0
                    break
            if baisegeshu > 20:
                baisegeshu = 0
                break
        baisegeshu = 0
        diyici = True
    return min
#纵方块数 = （下边界-上边界+1）//（纵边长+纵缝隙）
def zongfangkuai(zongbianchang,zongfengxi):
    geshu = (xiabianjie_waibu - shangbianjie_waibu + 1) // (zongbianchang + zongfengxi)
    if (xiabianjie_waibu - shangbianjie_waibu + 1) % (zongbianchang + zongfengxi)>20:
        geshu += 1
    return geshu
#横方块数 = （右边界-左边界+1）//（横边长+横缝隙）
def hengfangkuai(hengbianchang,hengfengxi):
    geshu = (youbianjie_waibu - zuobianjie_waibu + 1) // (hengbianchang + hengfengxi)
    if (youbianjie_waibu - zuobianjie_waibu + 1) % (hengbianchang + hengfengxi) > 20:
        geshu += 1
    return geshu

def kongfangkuai(zonggeshu,zongchang,hengfengxi,hengchang):#纵个数，纵长，横缝隙，横长
    #横长 < 白色个数 < 全长 - 横长 时 可以算作为空白方块  不然 break
    #在一条线上 碰到（不是白色的颜色 或 到了尽头）时 看看白色个数为几个，然后分配空白方块的个数和位置

    #如果在第一条线上已经知道所有空白方块在哪个方位 → 直接将 Y + 纵长    for循环时 把 Y的 跳跃能力调到 for i in range(上边界+20,上边界+20+（纵个数 * 纵长）+1,纵长)
    #如果在   起点
    baisegeshu = 0
    jilu = []
    qidian = []
    #真坐标是 X + 12
    #真坐标是 Y + 210
    for y in range(shangbianjie_waibu + 20, shangbianjie_waibu + 20 + ((zonggeshu-1) * zongchang) + 1 , zongchang):
        for x in range(zuobianjie_waibu,youbianjie_waibu):
            if zidian_waibu.get((x,y)) == baise:
                baisegeshu += 1
                if baisegeshu > hengchang:
                    jilu.append([x,y])
                    print("白色")
                    baisegeshu = 0
            else:
                if baisegeshu < hengfengxi+5:#如果白色个数比缝隙+5还小的话，那就是缝隙了
                    baisegeshu = 0
                else:
                    jilu.append([x,y])
                    print("家家爱极")
                    baisegeshu = 0
            if zidian_waibu.get((x,y))[0] != zidian_waibu.get((x,y))[1]:
                if x == youbianjie_waibu - 1:
                    qidian.append([x,y])
                    break
                if zidian_waibu.get((x+1,y)) == baise:
                    qidian.append([x,y])
        if baisegeshu > hengfengxi+5:   #如果空方块在最后一个位置时，记录
            jilu.append([x,y])
            baisegeshu = 0
    return jilu,qidian

def zhuanhua(zhen_kongfangkuai,qidian,hengchang,zongchang):#空方块列表，起点列表，横长，纵长
    #空方块的点在  Y坐标：（Y - 20）/ 纵长 + 1
    #空方块的点在  X坐标： X / 横长
    kongfangkuaizuobiao = []
    qidianzuobiao = []
    for i in range(len(zhen_kongfangkuai)):
        kongfangkuaizuobiao.append([(zhen_kongfangkuai[i][0] + 20 - zuobianjie_waibu) // hengchang, (zhen_kongfangkuai[i][1] - shangbianjie_waibu) // zongchang + 1])
    qidianzuobiao.append([(qidian[0][0] + 20 - zuobianjie_waibu) // hengchang, (qidian[0][1] - shangbianjie_waibu) // zongchang + 1])
    return kongfangkuaizuobiao, qidianzuobiao
#判断：若现状的长度 == 黑色方块数 即返回True，反之False
def panduan_re(liebiao):
    if len(liebiao) != linggeshu + 1:
        panduan = False
    else:
        panduan = True
    return panduan

    #return mubiao
#用于输出地图时，前期为了明明白白的看清楚地图的手段。（调试用）
def fangxiangjian(mubiao):
    changdu = len(mubiao)
    for i in range(changdu):
        if i == changdu - 1:
            break
        if mubiao[i][0] == mubiao[i+1][0]:
            if mubiao[i][1] < mubiao[i+1][1]:
                ditu[mubiao[i][0]][mubiao[i][1]] = "→"
            else:
                ditu[mubiao[i][0]][mubiao[i][1]] = "←"
        if mubiao[i][1] == mubiao[i+1][1]:
            if mubiao[i][0] < mubiao[i+1][0]:
                ditu[mubiao[i][0]][mubiao[i][1]] = "↓"
            else:
                ditu[mubiao[i][0]][mubiao[i][1]] = "↑"
    #print(ditu[0][0],ditu[0][1],ditu[1][0],ditu[1][1])
    print(ditu)
    #print('ok')

#算法
def digui(toubu,xianzhuang):#递归必须要设置return，而且是在每一个地方，一个if和没有if地方 都要设置return，  有条件判断的if
    #地图用外部的地图，所以global
    global ditu
    #p用于判断时机并return
    global p
    #若递归递到了退出的时机，那就进入这个判断中，使p加1，使整个递归函数准备退出
    if panduan_re(xianzhuang) == True:
        fangxiangjian(xianzhuang)
        print(xianzhuang)
        p += 1
        return xianzhuang

    if toubu[0] != 0:#上
        #隐藏在每一个判断与代码块中的退出程序
        if p == 1:
            return xianzhuang
        #----                 -------------
        #如果头部上面的方块是有效的！
        #即在现状中加入上面的方块
        #并在地图中显示为无效的方块
        if ditu[toubu[0] - 1][toubu[1]] == "0":
            xianzhuang.append([toubu[0] - 1,toubu[1]])
            ditu[xianzhuang[-1][0]][xianzhuang[-1][1]] = "1"
            #print(ditu)
            #进入下一个方块上的判断
            digui(xianzhuang[-1],xianzhuang)
    #左边的方块的判断
    if toubu[1] != 0:#左

        if p == 1:
            return xianzhuang

        if ditu[toubu[0]][toubu[1] - 1] == "0":
            xianzhuang.append([toubu[0],toubu[1] - 1])
            ditu[xianzhuang[-1][0]][xianzhuang[-1][1]] = '1'
            #print(ditu)



            digui(xianzhuang[-1],xianzhuang)
    #下面的方块的判断
    if toubu[0] != ditu_y - 1:#下

        if p == 1:
            return xianzhuang

        if ditu[toubu[0] + 1][toubu[1]] == "0":
            xianzhuang.append([toubu[0] + 1,toubu[1]])
            #print(ditu)
            #print(toubu[0],toubu[1])
            #print(toubu[0]+1,toubu[1])
            ditu[xianzhuang[-1][0]][xianzhuang[-1][1]] = "1"



            digui(xianzhuang[-1],xianzhuang)
    #右边的方块的判断
    if toubu[1] != ditu_x - 1:#右

        if p == 1:
            return xianzhuang

        if ditu[toubu[0]][toubu[1] + 1] == "0":
            xianzhuang.append([toubu[0],toubu[1] + 1])
            ditu[xianzhuang[-1][0]][xianzhuang[-1][1]] = "1"
            #print(ditu)



            digui(xianzhuang[-1],xianzhuang)

    #if toubu[0] != 0 and toubu[1] != 0 and toubu[0] != ditu_y -1 and toubu[1] != ditu_x -1:
        #if ditu[toubu[0] - 1][toubu[1]] != 0 and ditu[toubu[0]][toubu[1] - 1] != 0 and ditu[toubu[0] + 1][toubu[1]] != 0 and ditu[toubu[0]][toubu[1] + 1] != 0:
    #普通代码块的隐藏退出代码
    if p == 1:
        return xianzhuang
    #每一次判断所有方向后
    #好像这块代码没有必要
    #本来想的是每次进到了死路之后返回时 使地图中现在的点变为有效的点
    #并使现状变成之前一步
    #但是又觉得有用，因为递归是从头往下来的，所以先判断最先的一路，并查看第一路是否成功
    #不然就返回到上次十字路口，并试验下一个路口，如果下一个也不行，就到这里，退回到又上一次的路口
    ditu[xianzhuang[-1][0]][xianzhuang[-1][1]] = "0"
    #print(ditu)
    del xianzhuang[-1]

    #return xianzhuang
#从方块坐标到全屏像素坐标的转化
def shubiaozuobiao(xianzhuang,hengchang,zongchang,game_rect_0,game_rect_1):#现状，横长，纵长，game_rect 0 1
    qidian = True
    shubiaozuobiaolist = []
    for i in range(len(xianzhuang)):
        x = (xianzhuang[i][1]+1)*hengchang+12 + zuobianjie_waibu   + game_rect_0 - hengchang//2
        y = (xianzhuang[i][0]+1)*zongchang+210+ shangbianjie_waibu + game_rect_1 - zongchang//2
        shubiaozuobiaolist.append([x,y])
    #使转化成功的数据记录到文件中，并用按键精灵实现鼠标点击
    wenjian = open("D:/Study/python_study/waigua/xianzhuang.txt", "w+")
    for i in range(len(shubiaozuobiaolist)):
        wenjian.write(str(shubiaozuobiaolist[i][0])+"x"+str(shubiaozuobiaolist[i][1])+"y"+"\n")
    wenjian.close()
def errortext(hengchang,zongchang,game_rect_0,game_rect_1,kongfangkuaizuobiao):#现状，横长，纵长，game_rect 0 1
    shubiaozuobiaolist = []
    for i in range(len(kongfangkuaizuobiao)):
        x = (kongfangkuaizuobiao[i][1])*hengchang+12 + zuobianjie_waibu   + game_rect_0 - hengchang//2
        y = (kongfangkuaizuobiao[i][0])*zongchang+210+ shangbianjie_waibu + game_rect_1 - zongchang//2
        shubiaozuobiaolist.append([x,y])
    wenjian_1 = open("D:/Study/python_study/waigua/error.txt", "w+")
    for i in range(len(shubiaozuobiaolist)):
        wenjian_1.write(str(shubiaozuobiaolist[i][0])+"x"+str(shubiaozuobiaolist[i][1])+"y"+"\n")
    wenjian_1.close()
#------------------------------------------------------函数块的结束------------------------------------------------
#---------------------------------------------------------第二步--------------------------------------------------
#循环
while True:
    #截图
    src_image = ImageGrab.grab((game_rect[0] + 12, game_rect[1] + 210, game_rect[2] - 70, game_rect[3] - 135))
    print("游戏界面的位置：{}".format(game_rect))
    #src_image.show()
    #设置颜色的特征
    baise = [249, 249, 249]
    heise = [209, 209, 209]
    getcolor_1 = 0
    print("图片的大小：{}".format(src_image.size))
    #函数的启动
    zidian_waibu = yansezidian()
    shangbianjie_waibu,shangbianjie_2_waibu = tongji_shang()
    xiabianjie_waibu = tongji_xia()
    zuobianjie_waibu = tongji_zuo()
    youbianjie_waibu = tongji_you()
    #bianchang_1,fengxi_1 = bianchang(shangbianjie_2_waibu)
    zhen_bianchang = bianchang()
    zhen_fengxi = fengxi()
    zhen_zongfangkuai = zongfangkuai(zhen_bianchang+1,zhen_fengxi+3)
    zhen_hengfangkuai = hengfangkuai(zhen_bianchang,zhen_fengxi+2)
    #纵个数，纵长，横缝隙，横长
    zhen_kongfangkuai, zhen_qidian = kongfangkuai(zhen_zongfangkuai,zhen_bianchang+4+zhen_fengxi,zhen_fengxi+2,zhen_bianchang+2+zhen_fengxi)
    #空方块列表，起点列表，横长，纵长
    kongfangkuaizuobiao, qidianzuobiao = zhuanhua(zhen_kongfangkuai, zhen_qidian, zhen_bianchang+2+zhen_fengxi, zhen_bianchang+4+zhen_fengxi)
    print("上边界：{}，下边界：{}，左边界：{}，右边界：{}".format(shangbianjie_waibu,xiabianjie_waibu,zuobianjie_waibu,youbianjie_waibu))
    print("纵边长：{}，纵缝隙：{}，横纵长：{}，横缝隙：{}".format(zhen_bianchang+1,zhen_fengxi+3,zhen_bianchang,zhen_fengxi+2))
    print("整个方块属性：纵长：{}，横长：{}，纵个数：{}，横个数：{}".format(zhen_bianchang+4+zhen_fengxi,zhen_bianchang+2+zhen_fengxi,zhen_zongfangkuai,zhen_hengfangkuai))
    print("空方块像素坐标：{}".format(zhen_kongfangkuai))
    print("起点像素坐标：{}".format(zhen_qidian))
    print("空方块坐标：{}".format(kongfangkuaizuobiao))
    print("起点坐标：{}".format(qidianzuobiao))
    errortext(zhen_bianchang+2+zhen_fengxi,zhen_bianchang+4+zhen_fengxi,game_rect[0],game_rect[1],kongfangkuaizuobiao)
    #现状，横长，纵长，game_rect 0 1
    #zhen_bianchang+2+zhen_fengxi,zhen_bianchang+4+zhen_fengxi
    #heng_fangkuai, zong_fangkuai = lingfangkuai()
    #kongbai_list = kongfangkuai()
    #print(kongbai_list)
    #print(xindeyanselist)
    
    global p
    p = 0
    global ditu
    global xianzhuang_waibu
    xianzhuang_waibu = []

    #地图赋值
    ditu = zeros((zhen_zongfangkuai, zhen_hengfangkuai), dtype = "str")
    for i in range(len(ditu)):
        for j in range(len(ditu[0])):
            ditu[i][j] = "0"
    ditu_x = zhen_hengfangkuai
    ditu_y = zhen_zongfangkuai
    #起点赋值
    y, x = int(qidianzuobiao[0][0]) - 1, int(qidianzuobiao[0][1]) - 1
    toubu_x = y
    toubu_y = x
    ditu[x][y] = "1"
    #空白处赋值

    for i in range(len(kongfangkuaizuobiao)):
        y, x = int(kongfangkuaizuobiao[i][0]) - 1 , int(kongfangkuaizuobiao[i][1]) - 1
        ditu[x][y] = " "
    print(ditu)
    #空白处的个数记录
    linggeshu = 0
    for i in range(ditu_y):
        for j in range(ditu_x):
            if ditu[i][j] == "0":
                linggeshu += 1
    print("空白处的个数：{}".format(linggeshu))
    #现状的创建与赋值并输出
    xianzhuang = [] #现在的模样坐标群
    xianzhuang.append([toubu_y,toubu_x])

    toubu = xianzhuang[-1]  #头部坐标是现在的模样的最后一个坐标
    xianzhuang = digui(toubu,xianzhuang)
    #现状存于 文件 里
    shubiaozuobiao(xianzhuang,zhen_bianchang+2+zhen_fengxi,zhen_bianchang+4+zhen_fengxi,game_rect[0],game_rect[1])
    time.sleep(8)



