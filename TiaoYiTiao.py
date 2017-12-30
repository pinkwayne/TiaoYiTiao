import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
# import math
import time
import os


def pull_screenshot():
    """从手机截屏
    """
    os.system('adb shell screencap /sdcard/1.png')
    os.system('adb pull /sdcard/1.png')


def jump(distance):
    """根据距离计算按键时长，长按屏幕
    """
    press_time = int(distance * 1.35)
    cmd = f'adb shell input swipe 320 410 320 410 {press_time}'
    os.system(cmd)


def updatefig(*args):
    """等待1.5秒跳跃动画，然后更新手机画面
    """
    global updated

    if updated:
        print("跳~~~~")
        time.sleep(1.5)
        print("落地")
        pull_screenshot()
        im.set_array(update_data())
        updated = False
    return im,


def update_data():
    """Helper method of updatefig()
    """
    return np.array(Image.open('1.png'))


def onClick(event):
    global updated
    global click_count
    global last_click

    print(f'button={event.button}, x={event.x}, y={event.y}, xdata={event.xdata}, ydata={event.ydata}')

    click_count += 1
    # 第二次点画面，设定落脚点位置，计算距离，起跳，等待1.5秒动画
    if click_count == 2:
        click_count = 0
        last_xdata, last_ydata = last_click
        distance = np.sqrt((event.xdata - last_xdata)**2 +
        (event.ydata - last_ydata)**2)
        print(distance)
        jump(distance)
        updated = True

    # 第一次点画面，设定起跳位置
    else:
        last_click = (event.xdata, event.ydata)

if __name__ == '__main__':
    fig = plt.figure()
    updated = False  # 跳到了新位置没有

    # 初始化画面
    pull_screenshot()
    img = update_data()

    # 监听鼠标事件
    click_count = 0
    last_click = tuple()
    cid = fig.canvas.mpl_connect('button_press_event', onClick)

    # 显示画面，50毫秒刷新一次
    im = plt.imshow(img, animated=True)
    ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
    plt.show()
