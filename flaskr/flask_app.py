import base64
import io

import numpy as np
from flask import Flask, render_template, jsonify
from matplotlib import pyplot as plt

from python_reader.data_processing import DataProcessing


class MyApp:
    def __init__(self):
        self.app = Flask(__name__, template_folder='templates')
        self.app.debug = True
        self.app.static_folder = 'static'
        self.data_processing = DataProcessing()
        self.data_max, self.data_xyz = self.data_processing.get_data()
        self.header_max, self.header_xyz = self.data_processing.get_headers()
        self.i_xyz = 0
        self.i_max = 0

        @self.app.route('/')
        def display_table_and_plot():
            plot_data1, plot_data2 = self.data_processing.get_plots()
            return render_template('main_page.html',
                                   data_max=self.data_max,
                                   data_xyz=self.data_xyz,
                                   header_max=self.header_max,
                                   header_xyz=self.header_xyz,
                                   plot_data1=plot_data1,
                                   plot_data2=plot_data2)

        @self.app.route('/get_xyz')
        def get_xyz():
            return jsonify(values=self.get_xyz_())

        @self.app.route('/get_max')
        def get_max():
            return jsonify(values=self.get_max_())

        @self.app.route('/get_xyz_plot')
        def get_plots():
            xyz_value = self.get_xyz_()

            plt.plot(xyz_value)
            plt.ylabel('Wychylenie')
            plt.title('X, Y, Z')

            buffer_x = io.BytesIO()
            plt.savefig(buffer_x, format='png')
            buffer_x.seek(0)
            plot_x = base64.b64encode(buffer_x.read()).decode()
            plt.close()  # Close the plot to free up resources

            return jsonify(plot=plot_x)

    def get_max_(self):
        values = self.data_max
        values_len = len(self.data_max)
        values = values[self.i_max % values_len: self.i_max % values_len + 30]
        if values_len > 30:
            self.i_max += 1
        return values

    def get_xyz_(self):
        values = self.data_xyz
        values_len = len(self.data_xyz)
        values = values[self.i_xyz % values_len: self.i_xyz % values_len + 30]
        if values_len > 30:
            self.i_xyz += 1
        return values
    def run(self):
        self.app.static_folder = 'static'
        self.app.debug = True
        self.app.run()


my_app = MyApp()
# data_update_thread = threading.Thread(target=my_app.update_data_xyz)
# data_update_thread.start()
my_app.run()
