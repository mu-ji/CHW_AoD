import serial
import numpy as np
import math
import struct
import matplotlib.pyplot as plt
import binascii
import pandas as pd
import matplotlib.pyplot as plt


ser = serial.Serial('COM9', 115200)
rawFrame = []

node1_data = {'antenna_array_1':[], 'antenna_array_2':[], 'antenna_array_3':[], 'antenna_array_4':[]}
node2_data = {'antenna_array_1':[], 'antenna_array_2':[], 'antenna_array_3':[], 'antenna_array_4':[]}
node3_data = {'antenna_array_1':[], 'antenna_array_2':[], 'antenna_array_3':[], 'antenna_array_4':[]}


def pick_out_data(node_id, estimate_angle, antenna_array_id, time):
    if estimate_angle > 127:
        estimate_angle = estimate_angle - 256
    if node_id == 1:
        if antenna_array_id == 1:
            node1_data['antenna_array_1'].append(estimate_angle)
        elif antenna_array_id == 2:
            node1_data['antenna_array_2'].append(estimate_angle)
        elif antenna_array_id == 3:
            node1_data['antenna_array_3'].append(estimate_angle)
        elif antenna_array_id == 4:
            node1_data['antenna_array_4'].append(estimate_angle)
    
    elif node_id == 2:
        if antenna_array_id == 1:
            node2_data['antenna_array_1'].append(estimate_angle)
        elif antenna_array_id == 2:
            node2_data['antenna_array_2'].append(estimate_angle)
        elif antenna_array_id == 3:
            node2_data['antenna_array_3'].append(estimate_angle)
        elif antenna_array_id == 4:
            node2_data['antenna_array_4'].append(estimate_angle)
    
    elif node_id == 3:
        if antenna_array_id == 1:
            node3_data['antenna_array_1'].append(estimate_angle)
        elif antenna_array_id == 2:
            node3_data['antenna_array_2'].append(estimate_angle)
        elif antenna_array_id == 3:
            node3_data['antenna_array_3'].append(estimate_angle)
        elif antenna_array_id == 4:
            node3_data['antenna_array_4'].append(estimate_angle)
    else:
        return time
    time = time + 1
    return time


time = 0
while time <= 100:
    byte  = ser.read(1)        
    rawFrame += byte
    if rawFrame[-3:]==[255, 255, 255]:
        if len(rawFrame) == 6:
            print(time, rawFrame)
            node_id = rawFrame[0]
            estimate_angle = rawFrame[1]
            antenna_array_id = rawFrame[2]
            time = pick_out_data(node_id, estimate_angle, antenna_array_id, time)

            rawFrame = []
            #time = time + 1
        else:
            rawFrame = []

#plt.scatter(range(len(node1_data['antenna_array_1'])), node1_data['antenna_array_1'], label='node1_antenna_array_1')

fig, axs = plt.subplots(2, 4, figsize=(15, 10))
for i in range(4):
    data = node1_data['antenna_array_{}'.format(i+1)]
    mu, std = np.mean(data), np.std(data)
    count, bins, ignored = axs[0, i].hist(data, bins=30, density=False, alpha=1, color='g', label=f'node1_antenna_array_{i+1}')
    axs[0, i].set_xlim(-90, 90)
    x = np.linspace(-90, 90, 1000)
    p = np.exp(-((x - mu) ** 2) / (2 * std ** 2)) / (std * np.sqrt(2 * np.pi))
    axs[0, i].plot(x, p, 'k', linewidth=2)
    axs[0, i].set_title(f'Node1 Antenna Array {i+1}')
    axs[0, i].legend()

for i in range(4):
    data = node2_data['antenna_array_{}'.format(i+1)]
    mu, std = np.mean(data), np.std(data)
    count, bins, ignored = axs[1, i].hist(data, bins=30, density=False, alpha=1, color='g', label=f'node2_antenna_array_{i+1}')
    axs[1, i].set_xlim(-90, 90)
    x = np.linspace(-90, 90, 1000)
    p = np.exp(-((x - mu) ** 2) / (2 * std ** 2)) / (std * np.sqrt(2 * np.pi))
    axs[1, i].plot(x, p, 'k', linewidth=2)
    axs[1, i].set_title(f'Node2 Antenna Array {i}')
    axs[1, i].legend()


plt.tight_layout()
plt.show()

def cut_off_data(node_data):
    array_1_length = len(node_data['antenna_array_1'])
    array_2_length = len(node_data['antenna_array_2'])
    array_3_length = len(node_data['antenna_array_3'])
    array_4_length = len(node_data['antenna_array_4'])
    final_length = min(array_1_length, array_2_length, array_3_length, array_4_length)
    node_data['antenna_array_1'] = node_data['antenna_array_1'][:final_length]
    node_data['antenna_array_2'] = node_data['antenna_array_2'][:final_length]
    node_data['antenna_array_3'] = node_data['antenna_array_3'][:final_length]
    node_data['antenna_array_4'] = node_data['antenna_array_4'][:final_length]
    node_df = pd.DataFrame(node_data)
    return node_df


save_flag = input('Do you want to save the data? (y/n)')
if save_flag == 'y':
    number_of_node = input('Enter the number of node: ')
    if number_of_node == '1':
        node1_xangle = input('Enter the x angle of node1: ')
        node1_yangle = input('Enter the y angle of node1: ')
        print(node1_data)
        df = cut_off_data(node1_data)
        df.to_csv('AoD_experiment_data/one_node_experiment/node1_data_{}_{}_rotate.csv'.format(node1_xangle, node1_yangle))
    elif number_of_node == '2':
        node1_xangle = input('Enter the x angle of node1: ')
        node1_yangle = input('Enter the y angle of node1: ')
        node2_xangle = input('Enter the x angle of node2: ')
        node2_yangle = input('Enter the y angle of node2: ')
        node1_df = cut_off_data(node1_data)
        node2_df = cut_off_data(node2_data)
        node1_df.to_csv('AoD_experiment_data/two_node_experiment/node1_data_{}_{}.csv'.format(node1_xangle, node1_yangle))
        node2_df.to_csv('AoD_experiment_data/two_node_experiment/node2_data_{}_{}.csv'.format(node2_xangle, node2_yangle))