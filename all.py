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
global cpu_result, gpu_result, fps_result, network_result, dram_freq_result
global temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8 
global ctemp0, ctemp1, ctemp2, ctemp3, ctemp4, ctemp5, ctemp6, ctemp7
#############


print("///////////  ADB + 루팅 연결되어 있어야 작동 가능 //////////")
print("///////////  Track Time은 추적할 시간 입력(단위:초) //////////")
max_num = int(input('Track Time: '))

cpu_result = []
cpu_normal_result = []
dram_freq_result = []
gpu_result = []
gpu_clock_result = []
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
    
    cpu_n = []
    
    global cpu_result, gpu_result, fps_result, network_result, cpu_freq_result, gpu_clock_result
    global temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8
    global ctemp0, ctemp1, ctemp2, ctemp3, ctemp4, ctemp5, ctemp6, ctemp7
    old_network = 0
    old_fps = 0
    old_cpu_test = 0
    old_user = 0
    old_nice = 0
    old_system = 0
    old_idle = 0
    old_iowait = 0
    old_irq = 0
    old_softirq = 0
    old_steal = 0
    old_guest = 0
    old_guest_nice = 0
    d_user = 0
    d_nice = 0
    d_system = 0
    d_idle = 0
    d_iowait = 0
    d_irq = 0
    d_softirq = 0
    d_steal = 0
    d_guest = 0
    d_guest_nice = 0
    cur_cpu_usage = 0

    for i in range(num):
        # if 0: ## app cpu
        #     cpu_usage.append(device.shell("top -b -n1 | grep " + app_name + " | head -n1"))
        #     cpu_result.append(float((cpu_usage[i].split())[8])/max_cpu_usage*100)
        # else: ## total cpu
        #     cpu_usage.append(device.shell("top -n1 | grep idle | head -n1"))
        #     temp_data = cpu_usage[i].split()
        #     numbers = re.sub(r'[^0-9]', '', temp_data[4])
        #     if (max_cpu_usage-int(numbers)) < 0:
        #         numbers == max_cpu_usage
        #     cpu_result.append((max_cpu_usage-int(numbers))/max_cpu_usage*100)
        cpu_c = [0 for i in range(8)]
        cpu_n = [0 for i in range(8)]

        if 1:
            cpu_test =device.shell("cat /proc/stat")
            if i == 0:
                cpu_result.append(0) 
            else:                 
                old_c_temp = old_cpu_test.split()
                c_temp = cpu_test.split()
                cpu_cur_c = 0
                for j in range(8):
                    # for k in range(7):
                    old_user = int(old_c_temp[12+j*11])
                    old_nice = int(old_c_temp[13+j*11])
                    old_system = int(old_c_temp[14+j*11])
                    old_idle = int(old_c_temp[15+j*11])
                    old_iowait = int(old_c_temp[16+j*11])
                    old_irq = int(old_c_temp[17+j*11])
                    old_softirq = int(old_c_temp[18+j*11])
                    old_steal = int(old_c_temp[19+j*11])
                    old_guest = int(old_c_temp[20+j*11])
                    old_guest_nice = int(old_c_temp[21+j*11])

                    d_user = int(c_temp[12+j*11])
                    d_nice = int(c_temp[13+j*11])
                    d_system = int(c_temp[14+j*11])
                    d_idle = int(c_temp[15+j*11])
                    d_iowait = int(c_temp[16+j*11])
                    d_irq = int(c_temp[17+j*11])
                    d_softirq = int(c_temp[18+j*11])
                    d_steal = int(c_temp[19+j*11])
                    d_guest = int(c_temp[20+j*11])
                    d_guest_nice = int(c_temp[21+j*11])

                    previous_idle = old_idle + old_iowait
                    current_idle = d_idle + d_iowait

                    previous_non_idle = old_user + old_nice + old_system + old_irq + old_softirq + old_steal
                    current_non_idle = d_user + d_nice + d_system + d_irq + d_softirq + d_steal

                    previous_total = previous_idle + previous_non_idle
                    current_total = current_idle + current_non_idle

                    diff_total = current_total - previous_total
                    diff_idle = current_idle - previous_idle

                    cpu_c[j]= (diff_total - diff_idle) / diff_total * 100

                    
                    #     c_temp[12+k+j*11] = int(c_temp[12+k+j*11]) - int(old_c_temp[12+k+j*11])
                    # cpu_c[j] = (int(c_temp[12+j*11]) + int(c_temp[13+j*11]) + int(c_temp[14+j*11]) + int(c_temp[16+j*11]) + int(c_temp[17+j*11]) + int(c_temp[18+j*11])) / (int(c_temp[12+j*11]) + int(c_temp[13+j*11]) + int(c_temp[14+j*11])+ int(c_temp[15+j*11]) + int(c_temp[16+j*11]) + int(c_temp[17+j*11]) + int(c_temp[18+j*11])) * 100
                    cpu_cur_c = cpu_c[j] + cpu_cur_c

                cpu_result.append(cpu_cur_c/8)
                cur_cpu_usage = cpu_cur_c/8

            old_cpu_test = cpu_test

        if 1:
            if 0:
                cpu_result.append(0) 
                ctemp0.append(float(0))
                ctemp1.append(float(0))
                ctemp2.append(float(0))
                ctemp3.append(float(0))
                ctemp4.append(float(0))
                ctemp5.append(float(0))
                ctemp6.append(float(0))
                ctemp7.append(float(0))
                cpu_normal_result.append(0)
            elif 0:    
                ctemp0_usage.append(device.shell("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"))
                ctemp0.append(float((ctemp0_usage[i].split())[0]))
                ctemp0_max = device.shell("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
                cpu_n[0] =  (cpu_c[0] * ( int((ctemp0_usage[i].split())[0])/int(ctemp0_max)))
                # cpu_n.append(cpu_c[0] * ( int((ctemp0_usage[i].split())[0])/int(ctemp0_max)))

                # ctemp1_usage.append(device.shell("cat /sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq"))
                # ctemp1.append(float((ctemp1_usage[i].split())[0]))
                # ctemp1_max = device.shell("cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_max_freq")
                # cpu_n[1] = (cpu_c[1] * ( int((ctemp0_usage[i].split())[0])/int(ctemp1_max)))
                # # cpu_n.append(cpu_c[1] * ( int((ctemp0_usage[i].split())[0])/int(ctemp1_max)))
                
                # ctemp2_usage.append(device.shell("cat /sys/devices/system/cpu/cpu2/cpufreq/scaling_cur_freq"))
                # ctemp2.append(float((ctemp2_usage[i].split())[0]))
                # ctemp2_max = device.shell("cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_max_freq")
                # cpu_n[2] = (cpu_c[2] * ( int((ctemp2_usage[i].split())[0])/int(ctemp2_max)))
                # # cpu_n.append(cpu_c[2] * ( int((ctemp2_usage[i].split())[0])/int(ctemp2_max)))

                # ctemp3_usage.append(device.shell("cat /sys/devices/system/cpu/cpu3/cpufreq/scaling_cur_freq"))
                # ctemp3.append(float((ctemp3_usage[i].split())[0]))
                # ctemp3_max = device.shell("cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_max_freq")
                # cpu_n[3] = (cpu_c[3] * ( int((ctemp3_usage[i].split())[0])/int(ctemp3_max)))
                # # cpu_n.append(cpu_c[3] * ( int((ctemp3_usage[i].split())[0])/int(ctemp3_max)))
            
                ctemp4_usage.append(device.shell("cat /sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq"))
                ctemp4.append(float((ctemp4_usage[i].split())[0]))
                ctemp4_max = device.shell("cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_max_freq")
                cpu_n[4] = (cpu_c[4] * ( int((ctemp4_usage[i].split())[0])/int(ctemp4_max)))
                # cpu_n.append(cpu_c[4] * ( int((ctemp4_usage[i].split())[0])/int(ctemp4_max)))
                
                # ctemp5_usage.append(device.shell("cat /sys/devices/system/cpu/cpu5/cpufreq/scaling_cur_freq"))
                # ctemp5.append(float((ctemp5_usage[i].split())[0]))
                # ctemp5_max = device.shell("cat /sys/devices/system/cpu/cpu5/cpufreq/cpuinfo_max_freq")
                # cpu_n[5] = (cpu_c[5] * ( int((ctemp5_usage[i].split())[0])/int(ctemp5_max)))
                # # cpu_n.append(cpu_c[5] * ( int((ctemp5_usage[i].split())[0])/int(ctemp5_max)))
            
                ctemp6_usage.append(device.shell("cat /sys/devices/system/cpu/cpu6/cpufreq/scaling_cur_freq"))
                ctemp6.append(float((ctemp6_usage[i].split())[0]))
                ctemp6_max = device.shell("cat /sys/devices/system/cpu/cpu6/cpufreq/cpuinfo_max_freq")
                cpu_n[6] = (cpu_c[6] * ( int((ctemp6_usage[i].split())[0])/int(ctemp6_max)))
                # cpu_n.append(cpu_c[6] * ( int((ctemp6_usage[i].split())[0])/int(ctemp6_max)))
                
                # ctemp7_usage.append(device.shell("cat /sys/devices/system/cpu/cpu7/cpufreq/scaling_cur_freq"))
                # ctemp7.append(float((ctemp7_usage[i].split())[0]))
                # ctemp7_max = device.shell("cat /sys/devices/system/cpu/cpu7/cpufreq/cpuinfo_max_freq")
                # cpu_n[7] = (cpu_c[7] * ( int((ctemp7_usage[i].split())[0])/int(ctemp7_max)))
                # # cpu_n.append(cpu_c[7] * ( int((ctemp7_usage[i].split())[0])/int(ctemp7_max)))
                
                # cpu_normal_result.append((cpu_n[0] + cpu_n[1]+ cpu_n[2]+ cpu_n[3]+ cpu_n[4]+ cpu_n[5]+ cpu_n[6]+ cpu_n[7])/8)
                cpu_normal_result.append(( (cpu_n[0]*4) + (cpu_n[4] * 2) + (cpu_n[6]*2) )/8)
            else:
                ctemp0_usage.append(device.shell("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"))
                ctemp0.append(float((ctemp0_usage[i].split())[0]))
                ctemp0_max = device.shell("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")

                ctemp4_usage.append(device.shell("cat /sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq"))
                ctemp4.append(float((ctemp4_usage[i].split())[0]))
                ctemp4_max = device.shell("cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_max_freq")
                cpu_n[4] = (cpu_c[4] * ( int((ctemp4_usage[i].split())[0])/int(ctemp4_max)))

                ctemp6_usage.append(device.shell("cat /sys/devices/system/cpu/cpu6/cpufreq/scaling_cur_freq"))
                ctemp6.append(float((ctemp6_usage[i].split())[0]))
                ctemp6_max = device.shell("cat /sys/devices/system/cpu/cpu6/cpufreq/cpuinfo_max_freq")
                cpu_n[6] = (cpu_c[6] * ( int((ctemp6_usage[i].split())[0])/int(ctemp6_max)))

                total_max_freq = int(ctemp0_max)*4 + int(ctemp4_max)*2 + int(ctemp6_max)*2
                total_cur_freq = int((ctemp0_usage[i].split())[0])*4 + int((ctemp4_usage[i].split())[0])*2 + int((ctemp6_usage[i].split())[0])*2

                total_cpu_n = cur_cpu_usage * (total_cur_freq/total_max_freq) 

                cpu_normal_result.append(total_cpu_n)


        if 1:
            dram_freq = device.shell("su -c /data/local/tmp/clk_s.sh -d")
            # print((dram_freq.split())[1])
            dram_freq_result.append( int((dram_freq.split())[1]))

        if 1:
            gpu_usage.append(device.shell("cat /sys/devices/platform/18500000.mali/utilization"))
            gpu_result.append(float((gpu_usage[i].split())[0]))
            
            gpu_cur_clock =  device.shell("cat /sys/devices/platform/18500000.mali/clock")
            gpu_normal_usage = int(gpu_cur_clock)/702000 * float((gpu_usage[i].split())[0])
            gpu_clock_result.append( gpu_normal_usage)

        
        if 1:
            # if not str(device.shell("dumpsys SurfaceFlinger | grep Log ")):
            #     # fps_usage.append(device.shell("dumpsys SurfaceFlinger | grep default-format=4 "))
            # if str(device.shell("dumpsys SurfaceFlinger | grep transform-hint=04 | head -1 ")):
            if 0:    
                # print("/////////////////1////////////////")
                fps_usage.append(device.shell("dumpsys SurfaceFlinger | grep transform-hint=04 | head -1 "))
                ftemp_data = fps_usage[i].split()
                numbers = re.sub(r'[^0-9]', '', ftemp_data[3])
                fps_final = int(numbers) - old_fps

                # if int(fps_final) < 0 or int(fps_final) > 121: 
                #     fps_final = old_fps
                
                if int(fps_final) < 0:
                        fps_final = 0
                elif int(fps_final) > 121:
                        fps_final = 120
                # print("first : "+str(fps_final))
                fps_result.append(float(fps_final))
                old_fps = int(numbers)
            elif str(device.shell("dumpsys SurfaceFlinger | grep default-format=4 | head -1 ")):  # youtube, xbox
                # print(str(device.shell("dumpsys SurfaceFlinger | grep default-format=4 | head -1 ")))
                fps_usage.append(str(device.shell("dumpsys SurfaceFlinger | grep default-format=4 | head -1 ")))

                try:
                    ftemp_data = fps_usage[i].split()
                    # print(ftemp_data[3])

                    numbers = re.sub(r'[^0-9]', '', ftemp_data[3])
                    
                    fps_final = int(numbers) - old_fps

                    if int(fps_final) < 0:
                        fps_final = 0
                    elif int(fps_final) > 121:
                        fps_final = 120
                except:
                        fps_final = 0
                # print("first : "+str(fps_final))
                fps_result.append(float(fps_final))
                old_fps = int(numbers)
                        
            elif str(device.shell("dumpsys SurfaceFlinger | grep Log ")):      
                # print("/////////////////3////////////////")    
                fps_usage.append(device.shell("dumpsys SurfaceFlinger | grep Log "))
                ftemp_data = fps_usage[i].split()
                numbers = re.sub(r'[^0-9]', '', ftemp_data[2])
                # print("second: "+numbers)
            else:
                old_fps = 0
                fps_usage.append(str(old_fps))
                # print("/////////////////4////////////////")
                old_fps = old_fps
                numbers = old_fps
                fps_result.append(float(numbers))

        if 1:
            network_usage.append(device.shell("cat /proc/net/dev | grep rmnet1| tail -n1"))
            recv = (network_usage[i].split())[1]
            send = (network_usage[i].split())[9]
            network_temp = (int(recv) + int(send)) - old_network
            network_result.append(network_temp/1000)

            if network_temp != old_network:
                old_network = (int(recv) + int(send))

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
            
            # temp8_usage.append(device.shell("su -c cat /sys/class/thermal/thermal_zone8/temp"))
            # temp8.append(float((temp8_usage[i].split())[0]))
        
        time.sleep(0.75) #0.75 perfdog #gamebench



def shell_plot(x):

    
    plt.subplot(611)
    fps_result[0] = 0
    plt.plot(x, fps_result, 'C3')
    plt.title('FPS')
    
    plt.subplot(612)
    plt.plot(x, cpu_normal_result, 'C1')
    plt.title('CPU Usage')

    plt.subplot(613)
    plt.plot(x, ctemp0, 'r', label='cpu0')
    # plt.plot(x, ctemp1, 'r', label='cpu1')
    # plt.plot(x, ctemp2, 'r', label='cpu2')
    # plt.plot(x, ctemp3, 'r', label='cpu3')
    plt.plot(x, ctemp4, 'b', label='cpu4')
    # plt.plot(x, ctemp5, 'g', label='cpu5')
    plt.plot(x, ctemp6, 'g', label='cpu6')
    # plt.plot(x, ctemp7, 'b', label='cpu7')
    plt.title('CPU Freq')
    # plt.legend(loc='right')
    # plt.tight_layout()

    plt.subplot(615)
    plt.plot(x, gpu_clock_result, 'C10')
    plt.title('GPU Usage')

    plt.subplot(614)
    plt.plot(x, dram_freq_result, 'C4')
    plt.title('dram_freq')
#

    # plt.subplot(615)
    # network_result[0] = 0
    # plt.plot(x, network_result, 'C4')
    # plt.title('network')

    plt.subplot(616)
    plt.plot(x, temp0, 'C5', label='temp0')
    # plt.plot(x, temp1, 'C6', label='temp1')
    # plt.plot(x, temp2, 'C7', label='temp2')
    # plt.plot(x, temp3, 'C8', label='temp3')
    # plt.plot(x, temp4, 'C9', label='temp4')
    # plt.plot(x, temp5, 'C10', label='temp5')
    # plt.plot(x, temp6, 'C11', label='temp6')
    # plt.plot(x, temp7, 'C12', label='temp7')
    # plt.plot(x, temp8, 'C13', label='temp8')
    plt.title('temp')
    # plt.legend(loc="right")



    # plt.tight_layout()
    plt.show()

def data_avg(num):
    total_fps = 0
    for i in range(num):
        total_fps = int(fps_result[i]) + total_fps
    avg_fps = total_fps / num
    print("average fps : " + str(avg_fps))

    total_cpu = 0
    for i in range(num):
        total_cpu = int(cpu_result[i]) + total_cpu
    avg_cpu = total_cpu / num
    print("average cpu : " + str(avg_cpu))

    total_cpu_n = 0
    for i in range(num):
        total_cpu_n = int(cpu_normal_result[i]) + total_cpu_n
    avg_cpu_n = total_cpu_n / num
    print("average cpu normalized : " + str(avg_cpu_n))

    total_gpu = 0
    for i in range(num):
        total_gpu = int(gpu_result[i]) + total_gpu
    avg_gpu = total_gpu / num
    print("average gpu : " + str(avg_gpu))

    total_gpu_n = 0
    for i in range(num):
        total_gpu_n = int(gpu_clock_result[i]) + total_gpu_n
    avg_gpu_n = total_gpu_n / num
    print("average gpu normalized : " + str(avg_gpu_n))


    total_net = 0
    for i in range(num):
        total_net = int(network_result[i]) + total_net
    avg_net = total_net / num
    print("average network(KB/s) : " + str(avg_net))


def data_save(num):
    f = open('temp_record.txt', 'w')
    for i in range(num):
        f.write(str(temp0[i]) + "\n")
    f.write('------temp0 \n')

    # for i in range(num):
    #     f.write(str(temp1[i]) + "\n")
    # f.write('------temp1 \n')

    # for i in range(num):
    #     f.write(str(temp2[i]) + "\n")
    # f.write('------temp2 \n')

    # for i in range(num):
    #     f.write(str(temp3[i]) + "\n")
    # f.write('------temp3 \n')

    # for i in range(num):
    #     f.write(str(temp4[i]) + "\n")
    # f.write('------temp4 \n')

    # for i in range(num):
    #     f.write(str(temp5[i]) + "\n")
    # f.write('------temp5 \n')

    # for i in range(num):
    #     f.write(str(temp6[i]) + "\n")
    # f.write('------temp6 \n')

    # for i in range(num):
    #     f.write(str(temp7[i]) + "\n")
    # f.write('------temp7 \n')

    # for i in range(num):
    #     f.write(str(temp8[i]) + "\n")
    # f.write('------temp8 \n')
    
    # f.write(temp1)
    # f.write('------')
    # f.close()

    f = open('fps_record.txt', 'w')
    for i in range(num):
        f.write(str(fps_result[i]) + "\n")
    f.write('------fps \n')
    # f.close()


    # f = open('cpu_record.txt', 'w')
    # for i in range(num):
    #     f.write(str(cpu_result[i]) + "\n")
    # f.write('------cpu \n')
    # # f.close()

    f = open('cpu_normal_record.txt', 'w')
    for i in range(num):
        f.write(str(cpu_normal_result[i]) + "\n")
    f.write('------cpu normal \n')

    f = open('cpu_freq_0_record.txt', 'w')
    for i in range(num):
        f.write(str(ctemp0[i]) + "\n")
    f.write('------cpu freq 0 \n')

    f = open('cpu_freq_4_record.txt', 'w')
    for i in range(num):
        f.write(str(ctemp4[i]) + "\n")
    f.write('------cpu freq 4 \n')

    f = open('cpu_freq_6_record.txt', 'w')
    for i in range(num):
        f.write(str(ctemp6[i]) + "\n")
    f.write('------cpu freq 6 \n')

    # f = open('gpu_record.txt', 'w')
    # for i in range(num):
    #     f.write(str(gpu_result[i]) + "\n")
    # f.write('------gpu \n')


    f.close()

shell_repeat(max_num)
shell_plot(x)
data_save(max_num)
data_avg(max_num)