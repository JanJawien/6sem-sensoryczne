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
        with open('../flaskr/python_reader/acc_data/data_oddech1.pkl', 'rb') as file:
            data = pickle.load(file)
            file.close()

        max_lm35_data = data[data[:, 0] == 0.0]
        ada_data = data[data[:, 0] == 1.0]

        self.lm35_temp = max_lm35_data[:, 1]
        self.max_spo2 = max_lm35_data[:, 3]
        self.max_bpm = max_lm35_data[:, 4]

        self.x = ada_data[:, 2]
        self.y = ada_data[:, 3]
        self.z = ada_data[:, 4] - 9.8

        self.data_max = [self.lm35_temp, self.max_spo2, self.max_bpm]
        self.data_xyz = [self.x, self.y, self.z]
        self.data_max = [(self.data_max[0][i], self.data_max[1][i], self.data_max[2][i]) for i in
                         range(len(self.data_max[0]))]
        self.data_xyz = [(self.data_xyz[0][i], self.data_xyz[1][i], self.data_xyz[2][i]) for i in
                         range(len(self.data_xyz[0]))]

    def get_data(self):
        return self.max_bpm, self.max_spo2, self.lm35_temp, self.data_max, self.data_xyz

    def get_headers(self):
        return ['Temperature (LM35)', 'spO2 (MAX)', 'BPM (MAX)'], ['X', 'Y', 'Z']

    def get_plots(self):
        mean_spo2 = np.mean(self.max_spo2[self.max_spo2 != -1])
        std_spo2 = np.std(self.max_spo2[self.max_spo2 != -1])
        values = [mean_spo2, self.BASIC_SPO2_LEVEL]
        std = [std_spo2, 0]

        fig, ax = plt.subplots(1, 1)
        ax.bar(range(len(values)), values, yerr=std, align='center', alpha=0.6)
        ax.set_xlabel('X1')
        ax.set_ylabel('SpO2 (%)')
        ax.set_title('Level of SpO2')
        ax.set_ylim(80, 100)
        ax.set_xticks(range(len(values)), ['Measured value', 'Healthy value'])
        buffer1 = io.BytesIO()
        fig.savefig(buffer1, format='png')
        buffer1.seek(0)
        plot_data1 = base64.b64encode(buffer1.read()).decode()
        plt.close(fig)



        return plot_data1, plot_data2
