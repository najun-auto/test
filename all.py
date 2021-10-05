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

app_name = "com.google.android.youtube"
# app_name = "com.miHoYo.GenshinImpact"
cpu_result_file = "cpu_usage"
gpu_result_file = "gpu_usage"
fps_result_file = "fps"
recv_result_file = "recv"
send_result_file = "sned"
max_cpu_usage = 800
global cpu_result, gpu_result, fps_result, network_result
global temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8 
#############

max_num = 600

cpu_result = []
gpu_result = []
fps_result = []
network_result = []
temp0 = []
temp1 = []
temp2 = []
temp3 = []
temp4 = []
temp5 = []
temp6 = []
temp7 = []
temp8 = []
x = np.arange(0, max_num, 1)
##
def shell_repeat(num):
    cpu_usage = []
    gpu_usage = []
    fps_usage = []
    network_usage = []
    temp0_usage = []
    temp1_usage = []
    temp2_usage = []
    temp3_usage = []
    temp4_usage = []
    temp5_usage = []
    temp6_usage = []
    temp7_usage = []
    temp8_usage = []
    global cpu_result, gpu_result, fps_result, network_result
    global temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8
    old_network = 0
    for i in range(num):
        cpu_usage.append(device.shell("top -b -n1 | grep " + app_name + " | head -n1"))
        cpu_result.append(float((cpu_usage[i].split())[8])/max_cpu_usage*100)

        gpu_usage.append(device.shell("cat /sys/devices/platform/18500000.mali/utilization"))
        gpu_result.append(float((gpu_usage[i].split())[0]))
        
        # fps_usage.append(device.shell("dumpsys SurfaceFlinger | grep Log "))
        # temp_data = fps_usage[i].split()
        # numbers = re.sub(r'[^0-9]', '', temp_data[2])
        # fps_result.append(float(numbers))

        network_usage.append(device.shell("cat /proc/net/dev | grep rmnet1| tail -n1"))
        recv = (network_usage[i].split())[1]
        send = (network_usage[i].split())[9]
        network_temp = (int(recv) + int(send)) - old_network
        network_result.append(network_temp/1000/1000)

        if network_temp != old_network:
            old_network = (int(recv) + int(send))

        temp0_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone0/temp"))
        temp0.append(float((temp0_usage[i].split())[0]))

        temp1_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone1/temp"))
        temp1.append(float((temp1_usage[i].split())[0]))

        temp2_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone2/temp"))
        temp2.append(float((temp2_usage[i].split())[0]))

        temp3_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone3/temp"))
        temp3.append(float((temp3_usage[i].split())[0]))

        temp4_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone4/temp"))
        temp4.append(float((temp4_usage[i].split())[0]))

        temp5_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone5/temp"))
        temp5.append(float((temp5_usage[i].split())[0]))

        temp6_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone6/temp"))
        temp6.append(float((temp6_usage[i].split())[0]))

        temp7_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone7/temp"))
        temp7.append(float((temp7_usage[i].split())[0]))
        
        temp8_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone8/temp"))
        temp8.append(float((temp8_usage[i].split())[0]))

def shell_plot(x):
    
    # plt.subplot(511)
    # plt.plot(x, cpu_result, 'C1')
    # plt.title('CPU Usage')
    
    # plt.subplot(512)
    # plt.plot(x, gpu_result, 'C2')
    # plt.title('GPU Usage')

    # # plt.subplot(223)
    # # plt.plot(x, fps_result, 'C3')
    # # plt.title('FPS')

    # plt.subplot(514)
    # network_result[0] = 0
    # plt.plot(x, network_result, 'C4')
    # plt.title('network')

    plt.subplot(111)
    plt.plot(x, temp0, 'C5', label='temp0')
    plt.plot(x, temp1, 'C6', label='temp1')
    plt.plot(x, temp2, 'C7', label='temp2')
    plt.plot(x, temp3, 'C8', label='temp3')
    plt.plot(x, temp4, 'C9', label='temp4')
    plt.plot(x, temp5, 'C10', label='temp5')
    plt.plot(x, temp6, 'C11', label='temp6')
    plt.plot(x, temp7, 'C12', label='temp7')
    plt.plot(x, temp8, 'C13', label='temp8')
    plt.title('temp')
    plt.legend()

    plt.tight_layout()
    plt.show()

shell_repeat(max_num)
shell_plot(x)