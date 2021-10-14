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
global temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8 
global ctemp0, ctemp1, ctemp2, ctemp3, ctemp4, ctemp5, ctemp6, ctemp7
#############


print("///////////  ADB + 루팅 연결되어 있어야 작동 가능 //////////")
print("///////////  Track Time은 추적할 시간 입력(단위:초) //////////")
max_num = int(input('Track Time: '))

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
ctemp0 = []
ctemp1 = []
ctemp2 = []
ctemp3 = []
ctemp4 = []
ctemp5 = []
ctemp6 = []
ctemp7 = []

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
    ctemp0_usage = []
    ctemp1_usage = []
    ctemp2_usage = []
    ctemp3_usage = []
    ctemp4_usage = []
    ctemp5_usage = []
    ctemp6_usage = []
    ctemp7_usage = []
    
    global cpu_result, gpu_result, fps_result, network_result, cpu_freq_result
    global temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8
    global ctemp0, ctemp1, ctemp2, ctemp3, ctemp4, ctemp5, ctemp6, ctemp7
    old_network = 0
    for i in range(num):
        if 0: ## app cpu
            cpu_usage.append(device.shell("top -b -n1 | grep " + app_name + " | head -n1"))
            cpu_result.append(float((cpu_usage[i].split())[8])/max_cpu_usage*100)
        else: ## total cpu
            cpu_usage.append(device.shell("top -n1 | grep idle | head -n1"))
            temp_data = cpu_usage[i].split()
            numbers = re.sub(r'[^0-9]', '', temp_data[4])
            cpu_result.append((max_cpu_usage-int(numbers))/max_cpu_usage*100)
 
            
        if 1:
            ctemp0_usage.append(device.shell("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"))
            ctemp0.append(float((ctemp0_usage[i].split())[0]))

            # ctemp1_usage.append(device.shell("cat /sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq"))
            # ctemp1.append(float((ctemp1_usage[i].split())[0]))

            # ctemp2_usage.append(device.shell("cat /sys/devices/system/cpu/cpu2/cpufreq/scaling_cur_freq"))
            # ctemp2.append(float((ctemp2_usage[i].split())[0]))

            # ctemp3_usage.append(device.shell("cat /sys/devices/system/cpu/cpu3/cpufreq/scaling_cur_freq"))
            # ctemp3.append(float((ctemp3_usage[i].split())[0]))

            ctemp4_usage.append(device.shell("cat /sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq"))
            ctemp4.append(float((ctemp4_usage[i].split())[0]))

            # ctemp5_usage.append(device.shell("cat /sys/devices/system/cpu/cpu5/cpufreq/scaling_cur_freq"))
            # ctemp5.append(float((ctemp5_usage[i].split())[0]))

            # ctemp6_usage.append(device.shell("cat /sys/devices/system/cpu/cpu6/cpufreq/scaling_cur_freq"))
            # ctemp6.append(float((ctemp6_usage[i].split())[0]))

            ctemp7_usage.append(device.shell("cat /sys/devices/system/cpu/cpu7/cpufreq/scaling_cur_freq"))
            ctemp7.append(float((ctemp7_usage[i].split())[0]))

        gpu_usage.append(device.shell("cat /sys/devices/platform/18500000.mali/utilization"))
        gpu_result.append(float((gpu_usage[i].split())[0]))
        
        fps_usage.append(device.shell("dumpsys SurfaceFlinger | grep Log "))
        temp_data = fps_usage[i].split()
        numbers = re.sub(r'[^0-9]', '', temp_data[2])
        fps_result.append(float(numbers))

        # network_usage.append(device.shell("cat /proc/net/dev | grep rmnet1| tail -n1"))
        # recv = (network_usage[i].split())[1]
        # send = (network_usage[i].split())[9]
        # network_temp = (int(recv) + int(send)) - old_network
        # network_result.append(network_temp/1000/1000)

        # if network_temp != old_network:
        #     old_network = (int(recv) + int(send))

        if 1:
            temp0_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone0/temp"))
            temp0.append(float((temp0_usage[i].split())[0]))

            # temp1_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone1/temp"))
            # temp1.append(float((temp1_usage[i].split())[0]))

            # temp2_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone2/temp"))
            # temp2.append(float((temp2_usage[i].split())[0]))

            # temp3_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone3/temp"))
            # temp3.append(float((temp3_usage[i].split())[0]))

            # temp4_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone4/temp"))
            # temp4.append(float((temp4_usage[i].split())[0]))

            # temp5_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone5/temp"))
            # temp5.append(float((temp5_usage[i].split())[0]))

            # temp6_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone6/temp"))
            # temp6.append(float((temp6_usage[i].split())[0]))

            # temp7_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone7/temp"))
            # temp7.append(float((temp7_usage[i].split())[0]))
            
            temp8_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone8/temp"))
            temp8.append(float((temp8_usage[i].split())[0]))
        
        # time.sleep(1)



def shell_plot(x):

    
    plt.subplot(511)
    plt.plot(x, fps_result, 'C3')
    plt.title('FPS')
    
    plt.subplot(512)
    plt.plot(x, cpu_result, 'C1')
    plt.title('CPU Usage')

    plt.subplot(513)
    plt.plot(x, ctemp0, 'r', label='cpu0')
    # plt.plot(x, ctemp1, 'r', label='cpu1')
    # plt.plot(x, ctemp2, 'r', label='cpu2')
    # plt.plot(x, ctemp3, 'r', label='cpu3')
    plt.plot(x, ctemp4, 'g', label='cpu4')
    # plt.plot(x, ctemp5, 'g', label='cpu5')
    # plt.plot(x, ctemp6, 'g', label='cpu6')
    plt.plot(x, ctemp7, 'b', label='cpu7')
    plt.title('CPU Freq')
    # plt.legend(loc='right')
    # plt.tight_layout()

    plt.subplot(514)
    plt.plot(x, gpu_result, 'C10')
    plt.title('GPU Usage')


    # plt.subplot(514)
    # network_result[0] = 0
    # plt.plot(x, network_result, 'C4')
    # plt.title('network')

    plt.subplot(515)
    plt.plot(x, temp0, 'C5', label='temp0')
    # plt.plot(x, temp1, 'C6', label='temp1')
    # plt.plot(x, temp2, 'C7', label='temp2')
    # plt.plot(x, temp3, 'C8', label='temp3')
    # plt.plot(x, temp4, 'C9', label='temp4')
    # plt.plot(x, temp5, 'C10', label='temp5')
    # plt.plot(x, temp6, 'C11', label='temp6')
    # plt.plot(x, temp7, 'C12', label='temp7')
    plt.plot(x, temp8, 'C13', label='temp8')
    plt.title('temp')
    # plt.legend(loc="right")



    # plt.tight_layout()
    plt.show()
    
def data_save(num):
    f = open('temp_record.txt', 'w')
    for i in range(num):
        f.write(str(temp0[i]) + "\n")
    f.write('------temp0 \n')

    for i in range(num):
        f.write(str(temp1[i]) + "\n")
    f.write('------temp1 \n')

    for i in range(num):
        f.write(str(temp2[i]) + "\n")
    f.write('------temp2 \n')

    for i in range(num):
        f.write(str(temp3[i]) + "\n")
    f.write('------temp3 \n')

    for i in range(num):
        f.write(str(temp4[i]) + "\n")
    f.write('------temp4 \n')

    for i in range(num):
        f.write(str(temp5[i]) + "\n")
    f.write('------temp5 \n')

    for i in range(num):
        f.write(str(temp6[i]) + "\n")
    f.write('------temp6 \n')

    for i in range(num):
        f.write(str(temp7[i]) + "\n")
    f.write('------temp7 \n')

    for i in range(num):
        f.write(str(temp8[i]) + "\n")
    f.write('------temp8 \n')
    
    # f.write(temp1)
    # f.write('------')
    f.close()

shell_repeat(max_num)
shell_plot(x)
data_save(max_num)