import json
import io
import base64
import time

import numpy as np
import matplotlib.pyplot as plt
import pickle





class DataProcessing:
    BASIC_SPO2_LEVEL = 97
    BASIC_TEMP_VALUE = 36.6

    def __init__(self):
        with open('../flaskr/python_reader/data.pkl', 'rb') as file:
            data = pickle.load(file)
            file.close()

        max_lm35_data = data[data[:, 0] == 0.0]
        ada_data = data[data[:, 0] == 1.0]

        self.lm35_temp = max_lm35_data[:, 1]
        self.max_spo2 = max_lm35_data[:, 3]
        self.max_bpm = max_lm35_data[:, 4]

        self.x = ada_data[:, 2]
        self.y = ada_data[:, 3]
        self.z = ada_data[:, 4]

        self.data_max = [self.lm35_temp, self.max_spo2, self.max_bpm]
        self.data_xyz = [self.x, self.y, self.z]
        self.data_max = [(self.data_max[0][i], self.data_max[1][i], self.data_max[2][i]) for i in
                         range(len(self.data_max[0]))]
        self.data_xyz = [(self.data_xyz[0][i], self.data_xyz[1][i], self.data_xyz[2][i]) for i in
                         range(len(self.data_xyz[0]))]

    def get_data(self):
        return self.data_max, self.data_xyz

    def get_headers(self):
        return ['Temperature (LM35)', 'spO2 (MAX)', 'BPM (MAX)'], ['X', 'Y', 'Z']

    def get_plots(self):
        mean_spo2 = np.mean(self.max_spo2)
        std_spo2 = np.std(self.max_spo2)

        values = [mean_spo2, self.BASIC_SPO2_LEVEL]
        std = [std_spo2, 0]

        # Data for the second plot
        healthy_temp = [self.BASIC_TEMP_VALUE for _ in range(len(self.lm35_temp))]

        plt.bar(range(len(values)), values, yerr=std, align='center', alpha=0.6)
        plt.xlabel('X1')
        plt.ylabel('SpO2 (%)')
        plt.title('Level of SpO2')
        plt.ylim(80, 100)
        plt.xticks(range(len(values)), ['Measured value', 'Healthy value'])

        # Save Plot 1 to a buffer
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png')
        buffer1.seek(0)
        plot_data1 = base64.b64encode(buffer1.read()).decode()
        plt.close()  # Close the plot to free up resources

        # Temperature values
        plt.plot(range(len(self.lm35_temp)), self.lm35_temp, marker='o', label='Measured values')
        plt.plot(range(len(healthy_temp)), healthy_temp, label='Healthy value')
        plt.xlabel('Measurement')
        plt.ylabel('Temperature')
        plt.title('Temperature Values')
        plt.xticks(range(len(self.lm35_temp)), [str(i) for i in range(len(self.lm35_temp))])
        plt.ylim(min(36, int(min(self.lm35_temp) - 0.5)), max(38, int(max(self.lm35_temp) + 1)))
        plt.legend()

        # Save Plot 2 to a buffer
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        plot_data2 = base64.b64encode(buffer2.read()).decode()
        plt.close()  # Close the plot to free up resources

        print(plot_data1)

        return plot_data1, plot_data2
