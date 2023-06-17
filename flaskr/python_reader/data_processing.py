import json
import io
import base64
import numpy as np
import matplotlib.pyplot as plt


class DataProcessing:
    BASIC_SPO2_LEVEL = 97
    BASIC_TEMP_VALUE = 36.6

    def __init__(self):
        with open('python_reader/data.json') as file:
            data = json.load(file)

        self.lm35_temp_list = []
        self.max_temp_list = []
        self.max_spo2_list = []
        self.max_bpm_list = []
        self.x_list = []
        self.y_list = []
        self.z_list = []

        # Accessing the data and storing values into lists
        for item in data:
            lm35_temp = float(item['lm35_temp'])
            max_temp = float(item['max_temp'])
            max_spo2 = float(item['max_spo2'])
            max_bpm = float(item['max_bpm'])
            x = float(item['x'])
            y = float(item['y'])
            z = float(item['z'])

            self.lm35_temp_list.append(lm35_temp)
            self.max_temp_list.append(max_temp)
            self.max_spo2_list.append(max_spo2)
            self.max_bpm_list.append(max_bpm)
            self.x_list.append(x)
            self.y_list.append(y)
            self.z_list.append(z)


    def get_headers(self):
        return ['Temperature (LM35)', 'Temperature (MAX)', 'spO2 (MAX)', 'BPM (MAX)', 'X', 'Y', 'Z']

    def get_data(self):
        return [self.lm35_temp_list,
                self.max_temp_list,
                self.max_spo2_list,
                self.max_bpm_list,
                self.x_list,
                self.y_list,
                self.z_list]

    def get_plots(self):
        mean_spo2 = np.mean(self.max_spo2_list)
        std_spo2 = np.std(self.max_spo2_list)

        values = [mean_spo2, self.BASIC_SPO2_LEVEL]
        std = [std_spo2, 0]

        # Data for the second plot
        healthy_temp = [self.BASIC_TEMP_VALUE for _ in range(len(self.lm35_temp_list))]

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
        plt.plot(range(len(self.lm35_temp_list)), self.lm35_temp_list, marker='o', label='Measured values')
        plt.plot(range(len(healthy_temp)), healthy_temp, label='Healthy value')
        plt.xlabel('Measurement')
        plt.ylabel('Temperature')
        plt.title('Temperature Values')
        plt.xticks(range(len(self.lm35_temp_list)), [str(i) for i in range(len(self.lm35_temp_list))])
        plt.ylim(min(36, int(min(self.lm35_temp_list) - 0.5)), max(38, int(max(self.lm35_temp_list) + 1)))
        plt.legend()

        # Save Plot 2 to a buffer
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        plot_data2 = base64.b64encode(buffer2.read()).decode()
        plt.close()  # Close the plot to free up resources

        print(plot_data1)

        return plot_data1, plot_data2
