from queue import Queue
from shapely.geometry import Polygon, Point
from PIL import Image

iof_queue = [Queue()]
avaiof = [0]  # 每个车位的avaiof
# park_box_seq = [[1480, 393, 2608, 670, 2247, 913, 1191, 571, 0],
#                 [2213, 922, 1348, 637, 812, 746, 1568, 1233, 0]]  # 每一个parkbox[四个点的x,y+iof]
park_box_seq = [[]]
# park_car_box = [[0, 0, 120, 300], [120, 0, 240, 300]]
park_car_box = [()]

frame = 40  # 检测前frame帧
in_thres = 0.4
out_thres = 0.2


def addpt(x, y):
    if len(park_box_seq[-1]) == 9:
        # 创建一个新车位
        park_box_seq.append([])
        avaiof.append(0)
        iof_queue.append(Queue())
        park_car_box.append(())
    park_box_seq[-1].extend([x, y])
    if len(park_box_seq[-1]) == 8:
        # 将iof位记录为最小y值便于排序
        park_box_seq[-1].append(min(park_box_seq[-1][::2]))


def init():
    # 将车位按y值小的优先排序

    park_box_seq.sort(key=lambda x: x[-1], reverse=True)
    print(park_box_seq)
    print(park_car_box)
    print(avaiof)
    print(iof_queue)


def frameinit():
    # 每一帧开始时reset每个车位的iof
    for parkbox in park_box_seq:
        parkbox[-1] = 0


def caliof(box):
    # calculate iof

    # 打印检测框
    # for it in box:
    #     print(it, end=" ")
    # print(" ")
    target_area = Polygon(((box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])))
    maxiof, maxpos = 0, 0

    for i, parkbox in enumerate(park_box_seq, 1):
        # 生成两个多边形区域
        park_area = Polygon(
            ((parkbox[0], parkbox[1]), (parkbox[2], parkbox[3]), (parkbox[4], parkbox[5]), (parkbox[6], parkbox[7])))

        # 相交区域面积
        in_s = target_area.intersection(park_area).area
        iof = in_s / park_area.area
        # print(iof)    # 打印iof
        # 更新这帧这个停车位的iof         每帧开始时清零iof,并用每个target updateiof获得maxiof对avaiof update
        if iof > maxiof:
            maxiof = iof
            maxpos = i-1
    if maxiof > park_box_seq[maxpos][8]:
        park_car_box[maxpos] = box
        park_box_seq[maxpos][8] = maxiof


def checkiof():
    global avaiof
    global iof_queue

    # update iof_queue && return park or not
    print()
    for i in range(0, len(avaiof)):
        iof = park_box_seq[i][8]
        iof_queue[i].put(iof)
        avaiof_former = avaiof[i]
        if iof_queue[i].qsize() <= frame:
            if iof_queue[i].qsize() > 1:
                avaiof[i] *= (iof_queue[i].qsize()-1)
            avaiof[i] += iof
            avaiof[i] /= (iof_queue[i].qsize())
            print('第%d个车位此时的avaiof： %f  ， 没车（未到%d帧）' % (i + 1, avaiof[i], frame))
        else:
            ft = iof_queue[i].get()
            avaiof[i] += (iof - ft) / frame
            print('第%d个车位此时的avaiof： %f' % (i + 1, avaiof[i]))
            if avaiof[i] >= in_thres:
                # print "有车" in qt
                print('第%d个车位有车' % (i + 1))
                # 车位进入
                # if avaiof_former < in_thres:
                #     print('\033[1;31m此时车位%d进入车辆\033[0m' % (i+1))
            elif avaiof[i] <= out_thres:
                # print "没车" in qt
                print('第%d个车位没车' % (i + 1))
                # 车位离开
                # if avaiof_former > out_thres:
                #     print('\033[1;31m此时车位%d离开车辆\033[0m' % (i+1))


def cut_image():
    path = "pict/2.jpg"
    img = Image.open(path)
    # 坐标点可以根据自己的需要进行调整

    for i, n in enumerate(park_car_box, 1):
        temp = img.crop(n )
        # 分别保存多个小图片，路径可以根据自己的需要设计
        temp.save(path.replace(".jpg", str(i - 1) + '.jpg'))
    return True
