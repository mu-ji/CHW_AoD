import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

aoa_anchor_data = pd.read_csv('nRF5340_aoa_anchor_energy_consumption_VDD.csv')
aoa_node_data = pd.read_csv('nRF52833dk_aoa_node_energy_consumption.csv')

aod_anchor_data = pd.read_csv('nRF5340_aod_anchor_energy_consumption_VDD.csv')
aod_node_data = pd.read_csv('nRF52833dk_aod_node_energy_consumption.csv')

plt.plot(aoa_anchor_data['Timestamp(ms)'][:200000], aoa_anchor_data['Current(uA)'][:200000]/1000, label='AoA anchor current electricity')
plt.plot(aoa_node_data['Timestamp(ms)'][:200000], aoa_node_data['Current(uA)'][:200000]/1000, label='AoA node current electricity')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()

plt.plot(aod_anchor_data['Timestamp(ms)'][:200000], aod_anchor_data['Current(uA)'][:200000]/1000, label='AoD anchor current electricity(uA)')
plt.plot(aod_node_data['Timestamp(ms)'][:200000], aod_node_data['Current(uA)'][:200000]/1000, label='AoD node current electricity(uA)')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()

plt.plot(aoa_anchor_data['Timestamp(ms)'][:200000], aoa_anchor_data['Current(uA)'][:200000]/1000, label='AoA anchor current electricity(uA)')
plt.plot(aod_anchor_data['Timestamp(ms)'][:200000], aod_anchor_data['Current(uA)'][:200000]/1000, label='AoD anchor current electricity(uA)')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()

plt.plot(aoa_node_data['Timestamp(ms)'][:200000], aoa_node_data['Current(uA)'][:200000]/1000, label='AoA node current electricity(uA)')
plt.plot(aod_node_data['Timestamp(ms)'][:200000], aod_node_data['Current(uA)'][:200000]/1000, label='AoD node current electricity(uA)')
plt.xlabel('Time (ms)')
plt.ylabel('Current electricity (mA)')
plt.legend()
plt.grid()
plt.show()