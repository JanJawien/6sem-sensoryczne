from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64
from python_reader.data_processing import DataProcessing

app = Flask(__name__, template_folder='templates')


@app.route('/')
def display_table_and_plot():
    # Call the function to get the data for the table
    data_processing = DataProcessing()

    # Define the table headers
    # Generate the plot
    plot_data1, plot_data2 = data_processing.get_plots()
    data = data_processing.get_data()
    headers = data_processing.get_headers()

    return render_template('main_page.html', headers=headers, data=data, plot_data1=plot_data1, plot_data2=plot_data2)


if __name__ == '__main__':
    app.static_folder = 'static'
    app.debug = True
    app.run()