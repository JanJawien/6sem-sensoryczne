import json

import numpy as np
import matplotlib.pyplot as plt

BASIC_SPO2_LEVEL = 97
BASIC_TEMP_VALUE = 36.6

with open('data.json') as file:
    data = json.load(file)

lm35_temp_list = []
max_temp_list = []
max_spo2_list = []
max_bpm_list = []

# Accessing the data and storing values into lists
for item in data:
    lm35_temp = float(item['lm35_temp'])
    max_temp = float(item['max_temp'])
    max_spo2 = float(item['max_spo2'])
    max_bpm = float(item['max_bpm'])

    lm35_temp_list.append(lm35_temp)
    max_temp_list.append(max_temp)
    max_spo2_list.append(max_spo2)
    max_bpm_list.append(max_bpm)

# Printing the lists
print("lm35_temp_list:", lm35_temp_list)
print("max_temp_list:", max_temp_list)
print("max_spo2_list:", max_spo2_list)
print("max_bpm_list:", max_bpm_list)

mean_spo2 = np.mean(max_spo2_list)
std_spo2 = np.std(max_spo2_list)

print(mean_spo2)
print(std_spo2)

values = [mean_spo2, BASIC_SPO2_LEVEL]
std = [std_spo2, 0]

x = range(len(values))


# Data for the second plot
healthy_temp = [BASIC_TEMP_VALUE for i in range(len(lm35_temp_list))]

# Create subplots
fig, axs = plt.subplots(2, 1, figsize=(6, 8))

# SpO2 values
axs[0].bar(range(len(values)), values, yerr=std, align='center', alpha=0.6)
axs[0].set_ylabel('SpO2 (%)')
axs[0].set_title('Level of SpO2')
axs[0].set_xticks(range(len(values)))
axs[0].set_xticklabels(['Measured value', 'Healthy value'])
axs[0].set_ylim(80, 100)

# Temperature values
axs[1].plot(range(len(lm35_temp_list)), lm35_temp_list, marker='o', label='Measured values')
axs[1].plot(range(len(healthy_temp)), healthy_temp, label='Healthy value')
axs[1].set_xlabel('Measurement')
axs[1].set_ylabel('Temperature')
axs[1].set_title('Temperature Values')
axs[1].set_xticks(range(len(lm35_temp_list)))
axs[1].set_xticklabels(str(i) for i in range(len(lm35_temp_list)))
axs[1].set_ylim(min(36, int(min(lm35_temp_list) - 0.5)), max(38, int(max(lm35_temp_list) + 1)))
axs[1].legend()

plt.tight_layout()
plt.subplots_adjust(hspace=0.25)

plt.show()

print(int(min(lm35_temp_list) - 1))