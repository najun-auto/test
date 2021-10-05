# 패키지 선언
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random
import time
import re

from ppadb.client import Client as AdbClient
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device = devices[0]

# app_name = "com.google.android.youtube"
app_name = "com.miHoYo.GenshinImpact"
cpu_result_file = "cpu_usage"
gpu_result_file = "gpu_usage"
fps_result_file = "fps"
recv_result_file = "recv"
send_result_file = "sned"
max_cpu_usage = 800
global old_network
old_network = 0
global temp_avg, temp_count
temp_avg = temp_count = 0
#############

fig = plt.figure()     #figure(도표) 생성

ax = plt.subplot(331, xlim=(0, 50), ylim=(0, 100))
ax_2 = plt.subplot(332, xlim=(0, 50), ylim=(0, 100))
ax_3 = plt.subplot(333, xlim=(0, 50), ylim=(0, 100))
ax_4 = plt.subplot(334, xlim=(0, 50), ylim=(0, 100))
ax_5 = plt.subplot(335, xlim=(0, 50), ylim=(0, 100))

max_points = 50
max_points_2 = 50
max_points_3 = 50
max_points_4 = 50
max_points_5 = 50

line, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
line_2, = ax_2.plot(np.arange(max_points_2), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='red',ms=1)
line_3, = ax_3.plot(np.arange(max_points_3), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='orange',ms=1)
line_4, = ax_4.plot(np.arange(max_points_4), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='green',ms=1)
line_5, = ax_5.plot(np.arange(max_points_5), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='purple',ms=1)

ax.set_title('CPU Usage')
ax_2.set_title('GPU Usage')
ax_3.set_title('FPS')
ax_4.set_title('Network')
ax_5.set_title('Thermal')


def init():
    return line
def init_2():
    return line_2
def init_3():
    return line_3
def init_4():
    return line_4
def init_5():
    return line_5



def animate(i):

    cpu_usage = device.shell("top -b -n1 | grep " + app_name + " | head -n1")
    data = cpu_usage.split()
    y = float(data[8])/max_cpu_usage*100
    # y = 50
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)

    return line

def animate_2(i):

    gpu_usage = device.shell("cat /sys/devices/platform/18500000.mali/utilization")
    data = gpu_usage.split()
    y_2 = float(data[0])
    # y_2 = 50
    old_y_2 = line_2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    line_2.set_ydata(new_y_2)
    return line_2

def animate_3(i):

    fps = device.shell("dumpsys SurfaceFlinger | grep Log ")
    data = fps.split()
    numbers = re.sub(r'[^0-9]', '', data[2])
    y_3 = float(numbers)
    old_y_3 = line_3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    line_3.set_ydata(new_y_3)
    return line_3

def animate_4(i):

    global old_network

    recv_old = device.shell("cat /proc/net/dev | grep rmnet2| head -n1")
    recv_old = recv_old.split()
    recv = recv_old[1]

    send = recv_old[9]
    network = int(recv) + int(send)

    network_final = network - old_network

    if network != old_network:
        old_network = network

    y_4 = int(network_final)/1000/1000
    
    old_y_4 = line_4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    line_4.set_ydata(new_y_4)
    return line_4

def animate_5(i):

    global temp_avg, temp_count
    temp_final = 0
    for i in range(9):
        temp = device.shell("su -c cat /sys/class/thermal/thermal_zone"+str(i)+"/temp")
        temp_final = temp_final + int(re.sub(r'[^0-9]', '', temp))
    temp_fianl = temp_final / 9
    
    temp_count = temp_count + 1

    y_5 = int(temp_final)/10000
    temp_avg = (y_5 + temp_avg) 
    print("current temp: " + str(y_5) + " temp_sum : " + str(temp_avg) + " count: " + str(temp_count))
    old_y_5 = line_5.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
    line_5.set_ydata(new_y_5)
    return line_5

# anim = animation.FuncAnimation(fig, animate  , init_func= init ,frames=200, interval=50, blit=False)
# anim_2 = animation.FuncAnimation(fig, animate_2  , init_func= init_2 ,frames=200, interval=50, blit=False)
# anim_3 = animation.FuncAnimation(fig, animate_3  , init_func= init_3 ,frames=200, interval=100, blit=False)
# anim_4 = animation.FuncAnimation(fig, animate_4  , init_func= init_4 ,frames=200, interval=10, blit=False)
anim_5 = animation.FuncAnimation(fig, animate_5  , init_func= init_5 ,frames=200, interval=50, blit=False)

plt.show()