import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

aoa_anchor_data = pd.read_csv('aoa_anchor_energy_consumption.csv')
aoa_node_data = pd.read_csv('aoa_node_energy_consumption.csv')

aod_anchor_data = pd.read_csv('aod_anchor_energy_consumption.csv')
aod_node_data = pd.read_csv('aod_node_energy_consumption.csv')
aod_node_without_network_data = pd.read_csv('aod_node_without_net_energy_consumption.csv')

plt.plot(aoa_anchor_data['Timestamp(ms)'], aoa_anchor_data['Current(uA)']/1000, label='AoA anchor current electricity')
plt.plot(aoa_node_data['Timestamp(ms)'], aoa_node_data['Current(uA)']/1000, label='AoA node current electricity')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()

plt.plot(aod_anchor_data['Timestamp(ms)'], aod_anchor_data['Current(uA)']/1000, label='AoD anchor current electricity(uA)')
plt.plot(aod_node_data['Timestamp(ms)'], aod_node_data['Current(uA)']/1000, label='AoD node current electricity(uA)')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()

plt.plot(aoa_anchor_data['Timestamp(ms)'], aoa_anchor_data['Current(uA)']/1000, label='AoA anchor current electricity(uA)')
plt.plot(aod_anchor_data['Timestamp(ms)'], aod_anchor_data['Current(uA)']/1000, label='AoD anchor current electricity(uA)')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()

plt.plot(aoa_node_data['Timestamp(ms)'], aoa_node_data['Current(uA)']/1000, label='AoA node current electricity(uA)')
plt.plot(aod_node_data['Timestamp(ms)'], aod_node_data['Current(uA)']/1000, label='AoD node current electricity(uA)')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()

plt.plot(aod_node_data['Timestamp(ms)'], aod_node_data['Current(uA)']/1000, label='AoD node current electricity(uA)')
plt.plot(aod_node_without_network_data['Timestamp(ms)'], aod_node_without_network_data['Current(uA)']/1000, label='AoD node without network current electricity(uA)')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()

aod_consumption = (160e-6*6e-3 + 184e-6*6e-3 + 14e-3*3.1e-3 + (500e-3 - 14e-3 - 160e-6 - 184e-6)*1.8e-6)/500e-3
print(aod_consumption)

def aoa_consumption(n):
    return (168e-6*6e-3 + (10+3*n)*8e-6*6e-3 + (500e-3 - 168e-6 - (10+3*n)*8*1e-6)*1.8e-6)/500e-3
print(aoa_consumption(1))

node_number = range(1, 500, 1)
plt.plot(node_number, [aod_consumption]*len(node_number), label='AoD node current electricity(uA)')
plt.plot(node_number, [aoa_consumption(i) for i in node_number], label='AoA node current electricity(uA)')
plt.grid()
plt.legend()
plt.show()

aoa_node_mean_consumption = aoa_node_data['Current(uA)'].mean()
aoa_anchor_mean_consumption = aoa_anchor_data['Current(uA)'].mean()
aod_node_mean_consumption = aod_node_data['Current(uA)'].mean()   
aod_anchor_consumption = aod_anchor_data['Current(uA)'].mean()
aod_node_without_network_consumption = aod_node_without_network_data['Current(uA)'].mean()

print('aoa_node_mean_consumption:', aoa_node_mean_consumption)
print('aoa_anchor_mean_consumption:', aoa_anchor_mean_consumption)
print('aod_node_mean_consumption:', aod_node_mean_consumption)
print('aod_anchor_consumption:', aod_anchor_consumption)
print('aod_node_without_network_consumption:', aod_node_without_network_consumption)