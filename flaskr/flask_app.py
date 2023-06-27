import base64
import io

import numpy as np
from flask import Flask, render_template, jsonify
from matplotlib import pyplot as plt

from python_reader.data_processing import DataProcessing


class MyApp:
    BASIC_SPO2_LEVEL = 97
    BASIC_TEMP_VALUE = 36.6

    def __init__(self):
        self.app = Flask(__name__, template_folder='templates')
        self.app.debug = True
        self.app.static_folder = 'static'
        self.data_processing = DataProcessing()
        self.max_bpm, self.max_spo2, self.lm35_temp, self.data_max, self.data_xyz = self.data_processing.get_data()
        self.i_xyz = -35
        self.i_temp = -15
        self.i_spO2 = -15

        @self.app.route('/')
        def display_table_and_plot():
            return render_template('main_page.html')

        @self.app.route('/get_spO2_plot')
        def get_spo2_plot():
            spo2, self.i_spO2 = self.get_values(self.max_spo2, 15, self.i_spO2, -1)
            print(spo2)
            print(spo2[spo2 != -1])
            error = False
            mean_spo2 = np.mean(spo2[spo2 != -1])
            std_spo2 = np.std(spo2[spo2 != -1])
            if np.isnan(mean_spo2):
                mean_spo2 = 0
                std_spo2 = 0
                error = True
            values = [mean_spo2, self.BASIC_SPO2_LEVEL]
            std = [std_spo2, 0]

            fig, ax = plt.subplots(1, 1)
            ax.bar(range(len(values)), values, yerr=std, align='center', alpha=0.6)
            ax.set_xlabel('X1')
            ax.set_ylabel('SpO2 (%)')
            ax.set_title('Level of SpO2')
            ax.set_ylim(80, 100)
            ax.set_xticks(range(len(values)), ['Measured value', 'Healthy value'])

            buffer = io.BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            plot = base64.b64encode(buffer.read()).decode()
            plt.close(fig)
            data = {'healthy': self.BASIC_SPO2_LEVEL, 'measured': mean_spo2, 'std': std_spo2, 'error': error}
            print(data)

            return jsonify(plot=plot, data=data)

        @self.app.route('/get_temp_plot')
        def get_temp_plot():
            data_temp, self.i_temp = self.get_values(self.lm35_temp, 15, self.i_temp)
            healthy_temp = [self.BASIC_TEMP_VALUE for _ in range(len(data_temp))]

            fig, ax = plt.subplots(1, 1)
            try:
                ax.plot(range(len(data_temp)), data_temp, marker='o', label='Measured values')
                ax.plot(range(len(healthy_temp)), healthy_temp, label='Healthy value')
                ax.set_xlabel('Measurement')
                ax.set_ylabel('Temperature')
                ax.set_title('Temperature Values')
                ax.set_xticks(range(len(data_temp)), [str(i) for i in range(len(data_temp))])
                ax.set_ylim(min(36, int(min(data_temp) - 0.5)), max(38, int(max(data_temp) + 1)))
                ax.legend()
            except:
                print('waiting for data')
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            plot = base64.b64encode(buffer.read()).decode()
            plt.close(fig)
            data = {'healthy': self.BASIC_TEMP_VALUE, 'measured': np.mean(data_temp[data_temp != 0])}

            return jsonify(plot=plot, data=data)

        @self.app.route('/get_xyz_plot')
        def get_xyz_plot():
            xyz_value, self.i_xyz = self.get_values(self.data_xyz, 35, self.i_xyz)
            std_values = np.std(xyz_value, axis=0)
            std_values = {'x': std_values[0], 'y': std_values[0], 'z': std_values[0]}
            max_value = np.max(np.max(xyz_value, axis=0))
            min_value = np.min(np.min(xyz_value, axis=0))

            fig, ax = plt.subplots(1, 1)
            ax.plot(xyz_value)
            ax.set_ylabel('Wychylenie')
            ax.set_title('X, Y, Z')
            ax.set_ylim(min(min_value, -3), max(max_value, 3))
            ax.legend(['X', 'Y', 'Z'], loc='upper right')

            buffer_x = io.BytesIO()
            fig.savefig(buffer_x, format='png')
            buffer_x.seek(0)
            plot = base64.b64encode(buffer_x.read()).decode()
            plt.close(fig)  # Close the plot to free up resources

            return jsonify(plot=plot, std_values=std_values)

    def get_values(self, values, max_values, iterator, padding=0):
        values_len = len(values)
        values = values[max(0, iterator): min(iterator + max_values + 1, values_len)]

        current_length = len(values)
        if current_length < max_values:
            padding_needed = max_values - current_length
            if iterator < max_values:
                values = np.pad(values, (padding_needed, 0), mode='constant', constant_values=padding)
            else:
                values = np.pad(values, (0, padding_needed), mode='constant', constant_values=padding)
        iterator += 1
        if iterator >= values_len:
            iterator = -max_values
        return values, iterator

    def run(self):
        self.app.static_folder = 'static'
        self.app.debug = True
        self.app.run()


my_app = MyApp()
my_app.run()
