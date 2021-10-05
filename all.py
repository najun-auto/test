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
global cpu_result, gpu_result, fps_result, network_result 
#############

max_num = 50

cpu_result = []
gpu_result = []
fps_result = []
network_result = []
x = np.arange(0, max_num, 1)

def shell_repeat(num):
    cpu_usage = []
    gpu_usage = []
    fps_usage = []
    network_usage = []
    global cpu_result, gpu_result, fps_result, network_result
    old_network = 0
    for i in range(num):
        cpu_usage.append(device.shell("top -b -n1 | grep " + app_name + " | head -n1"))
        cpu_result.append(float((cpu_usage[i].split())[8])/max_cpu_usage*100)
        
        gpu_usage.append(device.shell("cat /sys/devices/platform/18500000.mali/utilization"))
        gpu_result.append(float((gpu_usage[i].split())[0]))
        
        fps_usage.append(device.shell("dumpsys SurfaceFlinger | grep Log "))
        temp_data = fps_usage[i].split()
        numbers = re.sub(r'[^0-9]', '', temp_data[2])
        fps_result.append(float(numbers))

        network_usage.append(device.shell("cat /proc/net/dev | grep rmnet2| tail -n1"))
        recv = (network_usage[i].split())[1]
        send = (network_usage[i].split())[9]
        network_temp = (int(recv) + int(send)) - old_network
        network_result.append(network_temp/1000/1000)

        if network_temp != old_network:
            old_network = (int(recv) + int(send))

    
def shell_plot(x):
    plt.subplot(221)
    plt.plot(x, cpu_result, 'o-')
    plt.title('CPU Usage')
    
    plt.subplot(222)
    plt.plot(x, gpu_result, '.-')
    plt.title('GPU Usage')

    plt.subplot(223)
    plt.plot(x, fps_result, '.-')
    plt.title('FPS')

    plt.subplot(224)
    network_result[0] = 0
    plt.plot(x, network_result, '.-')
    plt.title('network')

    plt.show()

shell_repeat(max_num)
shell_plot(x)