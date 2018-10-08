import win32gui
import win32api
import win32con
from PIL import ImageGrab,Image
import time
from numpy import *
from ctypes import *
import pyautogui

#gdi32 = windll.gdi32
global hwnd
hwnd = win32gui.FindWindow("TXGuiFoundation","腾讯手游助手【极速傲引擎】")
if not hwnd:
    print("Window not find!")
else:
    print("句柄：{}".format(hwnd))
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)
time.sleep(1)
game_rect = win32gui.GetWindowRect(hwnd)

def yansezidian():
    zidian = {}
    for i in range(549):
        for j in range(704):
            getcolor_1 = list(src_image.getpixel((i,j)))
            zidian[(i,j)] = getcolor_1
    return zidian
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

def zongfangkuai(zongbianchang,zongfengxi):
    geshu = (xiabianjie_waibu - shangbianjie_waibu + 1) // (zongbianchang + zongfengxi)
    if (xiabianjie_waibu - shangbianjie_waibu + 1) % (zongbianchang + zongfengxi)>20:
        geshu += 1
    return geshu
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
def panduan_re(liebiao):
    if len(liebiao) != linggeshu + 1:
        panduan = False
    else:
        panduan = True
    return panduan

    #return mubiao

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
    global ditu
    global p
    if panduan_re(xianzhuang) == True:
        fangxiangjian(xianzhuang)
        print(xianzhuang)
        p += 1
        return xianzhuang

    if toubu[0] != 0:#上

        if p == 1:
            return xianzhuang

        if ditu[toubu[0] - 1][toubu[1]] == "0":
            xianzhuang.append([toubu[0] - 1,toubu[1]])
            ditu[xianzhuang[-1][0]][xianzhuang[-1][1]] = "1"
            #print(ditu)

            digui(xianzhuang[-1],xianzhuang)

    if toubu[1] != 0:#左

        if p == 1:
            return xianzhuang

        if ditu[toubu[0]][toubu[1] - 1] == "0":
            xianzhuang.append([toubu[0],toubu[1] - 1])
            ditu[xianzhuang[-1][0]][xianzhuang[-1][1]] = '1'
            #print(ditu)



            digui(xianzhuang[-1],xianzhuang)

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
    if p == 1:
        return xianzhuang
    ditu[xianzhuang[-1][0]][xianzhuang[-1][1]] = "0"
    #print(ditu)
    del xianzhuang[-1]

    #return xianzhuang
def shubiaozuobiao(xianzhuang,hengchang,zongchang,game_rect_0,game_rect_1):#现状，横长，纵长，game_rect 0 1
    qidian = True
    shubiaozuobiaolist = []
    for i in range(len(xianzhuang)):
        x = (xianzhuang[i][1]+1)*hengchang+12 + zuobianjie_waibu   + game_rect_0 - hengchang//2
        y = (xianzhuang[i][0]+1)*zongchang+210+ shangbianjie_waibu + game_rect_1 - zongchang//2
        shubiaozuobiaolist.append([x,y])
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
while True:
    src_image = ImageGrab.grab((game_rect[0] + 12, game_rect[1] + 210, game_rect[2] - 70, game_rect[3] - 135))
    print("游戏界面的位置：{}".format(game_rect))
    #src_image.show()
    baise = [249, 249, 249]
    heise = [209, 209, 209]
    getcolor_1 = 0
    print("图片的大小：{}".format(src_image.size))
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

    #地图
    ditu = zeros((zhen_zongfangkuai, zhen_hengfangkuai), dtype = "str")
    for i in range(len(ditu)):
        for j in range(len(ditu[0])):
            ditu[i][j] = "0"
    ditu_x = zhen_hengfangkuai
    ditu_y = zhen_zongfangkuai
    #起点
    y, x = int(qidianzuobiao[0][0]) - 1, int(qidianzuobiao[0][1]) - 1
    toubu_x = y
    toubu_y = x
    ditu[x][y] = "1"
    #空白处

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

    xianzhuang = [] #现在的模样坐标群
    xianzhuang.append([toubu_y,toubu_x])

    toubu = xianzhuang[-1]  #头部坐标是现在的模样的最后一个坐标
    xianzhuang = digui(toubu,xianzhuang)

    #现状存于 文件里




    shubiaozuobiao(xianzhuang,zhen_bianchang+2+zhen_fengxi,zhen_bianchang+4+zhen_fengxi,game_rect[0],game_rect[1])
    time.sleep(8)



