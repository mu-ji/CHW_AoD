import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

def generate_position(distance, node_data):
    array_1_mean = np.mean(node_data['antenna_array_1'])
    array_1_var = np.var(node_data['antenna_array_1'])
    array_2_mean = np.mean(node_data['antenna_array_2'])
    array_2_var = np.var(node_data['antenna_array_2'])
    array_3_mean = np.mean(node_data['antenna_array_3'])
    array_3_var = np.var(node_data['antenna_array_3'])
    array_4_mean = np.mean(node_data['antenna_array_4'])
    array_4_var = np.var(node_data['antenna_array_4'])

    array_1_weight = array_3_var/(array_1_var + array_3_var)
    array_3_weight = array_1_var/(array_1_var + array_3_var)
    array_2_weight = array_4_var/(array_2_var + array_4_var)
    array_4_weight = array_2_var/(array_2_var + array_4_var)

    total_estimate_x = distance*math.tan((array_1_mean*array_1_weight + array_3_mean*array_3_weight)*np.pi/180)
    total_estimate_y = distance*math.tan((array_2_mean*array_2_weight + array_4_mean*array_4_weight)*np.pi/180)

    x_list = []
    y_list = []
    sample_num = len(node_data['antenna_array_1'])
    for i in range(sample_num):
        x_list.append(distance*math.tan((node_data['antenna_array_1'][i]*array_1_weight + node_data['antenna_array_3'][i]*array_3_weight)*np.pi/180))
        y_list.append(distance*math.tan((node_data['antenna_array_2'][i]*array_2_weight + node_data['antenna_array_4'][i]*array_4_weight)*np.pi/180))
    
    return x_list, y_list, total_estimate_x, total_estimate_y
def one_node_visualization(distance, node1_xangle, node1_yangle):
    node1_data = pd.read_csv('AoD_experiment_data/one_node_experiment/node1_data_{}_{}.csv'.format(node1_xangle, node1_yangle))

    array_1_angle = node1_data['antenna_array_1']
    array_2_angle = node1_data['antenna_array_2']
    array_3_angle = node1_data['antenna_array_3']
    array_4_angle = node1_data['antenna_array_4']

    array_1_est_x = []
    array_2_est_y = []
    array_3_est_x = []
    array_4_est_y = []

    for i in range(len(array_1_angle)):
        #if array_1_angle[i] > 80 or array_1_angle[i] < -80:
        #    array_1_angle[i] = array_3_angle[i]
        array_1_est_x.append(distance*math.tan(array_1_angle[i]*np.pi/180))
        #if array_2_angle[i] > 80 or array_2_angle[i] < -80:
        #    array_2_angle[i] = array_4_angle[i]
        array_2_est_y.append(distance*math.tan(array_2_angle[i]*np.pi/180))
        #if array_3_angle[i] > 80 or array_3_angle[i] < -80:
        #    array_3_angle[i] = array_1_angle[i]
        array_3_est_x.append(distance*math.tan(array_3_angle[i]*np.pi/180))
        #if array_4_angle[i] > 80 or array_4_angle[i] < -80:
        #    array_4_angle[i] = array_2_angle[i]
        array_4_est_y.append(distance*math.tan(array_4_angle[i]*np.pi/180))

    node_1_x, node_1_y, node_1_estimate_x, node_1_estimate_y = generate_position(distance, node1_data)

    #plt.scatter(array_1_est_x, array_2_est_y, color = 'r', label='est according 1 and 2')
    #plt.scatter(array_1_est_x, array_4_est_y, color = 'b', label='est according 1 and 4')
    #plt.scatter(array_3_est_x, array_2_est_y, color = 'g', label='est according 3 and 2')
    #plt.scatter(array_3_est_x, array_4_est_y, color = 'y', label='est according 3 and 4')
    plt.scatter(node_1_estimate_x, node_1_estimate_y, color = 'k', label='estimate position')

    node1_xangle = node1_xangle*math.pi/180
    node1_yangle = node1_yangle*math.pi/180

    node_1_true_x = distance*math.tan(node1_xangle)
    node_1_true_y = distance*math.tan(node1_yangle)
    plt.scatter(node_1_true_x, node_1_true_y, color = 'b', label='true position')

    plt.plot([node_1_estimate_x, node_1_true_x], [node_1_estimate_y, node_1_true_y], color='r', linestyle='--')

    #plt.xlim(-2*distance, 2*distance)
    #plt.ylim(-2*distance,2*distance)
    plt.legend()
    
    return
for x in [0, -10, -20, -30, -40]:
    for y in [0, 10]:
#for x in [0]:
#    for y in [0, -10, -20, -30, -40]:
        one_node_visualization(2, x, y)
plt.grid()
plt.xlim(-2,2)
plt.ylim(-2,2)
plt.show()