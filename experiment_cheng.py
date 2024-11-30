import serial
import numpy as np
import math
import struct
import matplotlib.pyplot as plt
import binascii

import matplotlib.pyplot as plt
from math import pi, atan2, sqrt
from scipy.linalg import eig
#COM9 is nrf5340 receiver
ser = serial.Serial('COM9', 115200)

import cmath

SPEED_OF_LIGHT  = 299792458
num_iterations = 200     # 进行的循环次数
iteration = 0

rawFrame = []

all_data = {
    'I_data': [],
    'Q_data': [],
    'rssi' : [],
    'pattern' : []
}

#data = np.load('Cheng_data/data/nothing_Idata_0.npz')
#print(data['arr_0'])

num_samples = 88
data_index = 0
while True:
    byte  = ser.read(1)        
    rawFrame += byte
    #print(len(rawFrame))
    if rawFrame[-3:]==[255, 255, 255]:
        if len(rawFrame) == 4*num_samples+8:
            received_data = rawFrame[:4*num_samples]
            num_samples = 88

            I_data = np.zeros(num_samples, dtype=np.int16)
            Q_data = np.zeros(num_samples, dtype=np.int16)
            for i in range(num_samples):
                (I) = struct.unpack('>h', bytes(received_data[4*i+2:4*i+4]))
                (Q) = struct.unpack('>h', bytes(received_data[4*i:4*i+2]))
                #print(phase)
                #print((received_data[4*i+2] << 8) | received_data[4*i+3])
                #phase_data[i] = (received_data[4*i+2] << 8) | received_data[4*i+3]
                I_data[i] = I[0]
                Q_data[i] = Q[0]

            I_data = I_data.astype(np.float32)
            Q_data = Q_data.astype(np.float32)

            all_data['I_data'].append(I_data)
            all_data['Q_data'].append(Q_data)
            
            reference_I = I_data[:8]
            reference_Q = Q_data[:8]

            ant0_I = I_data[9:88:8]
            ant0_Q = Q_data[9:88:8]

            ant1_I = I_data[11:88:8]
            ant1_Q = Q_data[11:88:8]

            ant2_I = I_data[13:88:8]
            ant2_Q = Q_data[13:88:8]

            ant3_I = I_data[15:88:8]
            ant3_Q = Q_data[15:88:8]

            def normalization(ant_I, ant_Q):
                # 计算幅度
                amplitude = np.sqrt(ant_I**2 + ant_Q**2)
                # 归一化 I 和 Q 分量
                norm_I = ant_I / amplitude
                norm_Q = ant_Q / amplitude
                return norm_I, norm_Q

            def ant_IQ_norm(ant_I_array, ant_Q_array):
                for i in range(len(ant_I_array)):
                    ant_I_array[i], ant_Q_array[i] = normalization(ant_I_array[i], ant_Q_array[i])
                return ant_I_array, ant_Q_array
            
            # normalize three antenna IQ data, only consider phase information

            reference_I, reference_Q = ant_IQ_norm(reference_I, reference_Q)

            ant0_I, ant0_Q = ant_IQ_norm(ant0_I, ant0_Q)
            ant1_I, ant1_Q = ant_IQ_norm(ant1_I, ant1_Q)
            ant2_I, ant2_Q = ant_IQ_norm(ant2_I, ant2_Q)
            ant3_I, ant3_Q = ant_IQ_norm(ant3_I, ant3_Q)
            
            #from the reference IQ vector pattern, there is a small change between every us except pi/2 caused by 250KHz frequency shift

            def calculate_angle(I1, Q1, I2, Q2):
                # 计算归一化后的点积
                dot_product = I1 * I2 + Q1 * Q2
                
                # 计算 cos(θ)
                cos_theta = np.clip(dot_product, -1.0, 1.0)
                
                # 计算角度 (弧度)
                theta = np.arccos(cos_theta)

                # 返回角度（可选：将弧度转为角度）
                angle_in_degrees = np.degrees(theta)
                
                return theta
        
            ref_theta_array = np.zeros(4)
            for i in range(4):
                ref_theta_array[i] = calculate_angle(reference_I[i], reference_Q[i], reference_I[i+4], reference_Q[i+4])
            # in every us, the IQ vector will rotate pi/2 + a small error angle
            angle_change_1us = np.mean(ref_theta_array)/4
            print('angle_change_1us:',angle_change_1us)
            # this function helps to compensate the 250KHz and a small error angle
            def rotate_vector(I, Q, theta):
                I_new = I * np.cos(theta) - Q * np.sin(theta)
                Q_new = I * np.sin(theta) + Q * np.cos(theta)
                
                return I_new, Q_new
        
            def compensate_phase(ant_I, ant_Q, angle_change_1us):
                for i in range(len(ant_I)):
                    rotate_angle = i*(3.14/2 + angle_change_1us)*8
                    ant_I[i], ant_Q[i] = rotate_vector(ant_I[i], ant_Q[i], -rotate_angle)
                return ant_I, ant_Q

            i = 9 
            I_need = I_data[9:88:2]
            Q_need = Q_data[9:88:2]
            I_need, Q_need = compensate_phase(I_need, Q_need, -2*(np.pi/2+angle_change_1us))
            ax1 = plt.subplot(121)
            ax1.plot(I_need, Q_need)
            ax2 = plt.subplot(122)
            ax2.clear()
            ax2.plot(I_need, Q_need)
            experiment_name = 'nothing'
            if data_index <= 10:
                plt.savefig('Cheng_data/figure/{}_result_{}.png'.format(experiment_name, data_index))
                np.savez('Cheng_data/data/{}_Idata_{}.npz'.format(experiment_name, data_index), I_need)
                np.savez('Cheng_data/data/{}_Qdata_{}.npz'.format(experiment_name, data_index), Q_need)
            #plt.show()
            data_index += 1
            
            ant0_I_mean, ant0_Q_mean = np.mean(ant0_I), np.mean(ant0_Q)
            ant1_I_mean, ant1_Q_mean = np.mean(ant1_I), np.mean(ant1_Q)
            ant2_I_mean, ant2_Q_mean = np.mean(ant2_I), np.mean(ant2_Q)
            ant3_I_mean, ant3_Q_mean = np.mean(ant3_I), np.mean(ant3_Q)

            rotate_angle_1_0 = 2*(np.pi/2 + angle_change_1us) #+ np.radians(24)
            rotate_angle_2_0 = 4*(np.pi/2 + angle_change_1us)
            rotate_angle_3_0 = 6*(np.pi/2 + angle_change_1us) #+ np.radians(24)

            ant1_I_mean, ant1_Q_mean = rotate_vector(ant1_I_mean, ant1_Q_mean, -rotate_angle_1_0)
            ant2_I_mean, ant2_Q_mean = rotate_vector(ant2_I_mean, ant2_Q_mean, -rotate_angle_2_0)
            ant3_I_mean, ant3_Q_mean = rotate_vector(ant3_I_mean, ant3_Q_mean, -rotate_angle_3_0)
            
            ant0_I_mean, ant0_Q_mean = normalization(ant0_I_mean, ant0_Q_mean)
            ant1_I_mean, ant1_Q_mean = normalization(ant1_I_mean, ant1_Q_mean)
            ant2_I_mean, ant2_Q_mean = normalization(ant2_I_mean, ant2_Q_mean)
            ant3_I_mean, ant3_Q_mean = normalization(ant1_I_mean, ant3_Q_mean)
            #for i in range(len(ant0_I)):

            def steering_vector(alpha):
                j = 1j  # 复数单位
                return np.array([1, cmath.exp(-j * 2 * np.pi * 2.4e9 * (0.0375*np.sin(alpha)/SPEED_OF_LIGHT)), cmath.exp(-j * 2 * np.pi * 2.4e9 * 2*(0.0375*np.sin(alpha)/SPEED_OF_LIGHT))])

            def DoA_algorithm(ant0_I_mean, ant0_Q_mean, ant1_I_mean, ant1_Q_mean, ant2_I_mean, ant2_Q_mean):
                ant0_theta = cmath.phase(complex(ant0_I_mean, ant0_Q_mean))
                ant1_theta = cmath.phase(complex(ant1_I_mean, ant1_Q_mean))
                ant2_theta = cmath.phase(complex(ant2_I_mean, ant2_Q_mean))
                ant3_theta = cmath.phase(complex(ant3_I_mean, ant3_Q_mean))

                ant1_theta = ant1_theta - ant0_theta
                ant2_theta = ant2_theta - ant0_theta
                ant3_theta = ant3_theta - ant0_theta
                ant0_theta = 0

                received_signal = np.array([cmath.exp(1j*ant0_theta), cmath.exp(1j*ant1_theta), cmath.exp(1j*ant2_theta)])
                angle_list = [np.radians(i) for i in range(-90, 90)]
                y_alpha_list = []
                for alpha in angle_list:
                    y_alpha = steering_vector(alpha)[0]*received_signal[0] + steering_vector(alpha)[1]*received_signal[1] + steering_vector(alpha)[2]*received_signal[2]
                    y_alpha_list.append(y_alpha)
                #print(y_alpha_list)
                #plt.plot([i for i in range(-90, 90)], y_alpha_list)
                #plt.show()

                return [i for i in range(-90, 90)][np.argmax(np.array(y_alpha_list))]
            
            angle = DoA_algorithm(ant0_I_mean, ant0_Q_mean, ant1_I_mean, ant1_Q_mean, ant2_I_mean, ant2_Q_mean)
            print('DoA:', angle)

            
        rawFrame = []
        iteration = iteration + 1
    if len(all_data['I_data']) == num_iterations:
        all_data['I_data'] = np.array(all_data['I_data'])
        all_data['Q_data'] = np.array(all_data['Q_data'])
        all_data['rssi'] = np.array(all_data['rssi'])
        all_data['pattern'] = ['42,43,44,41']

        np.savez('IQ_Raw_data/60_data.npz', **all_data)
        break
