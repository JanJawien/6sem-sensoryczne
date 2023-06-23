updateXYZPlot()
updateSpO2Plot()
updateTempPlot()

function updateXYZPlot() {
            $.ajax({
                url: '/get_xyz_plot',
                success: function(response) {
                    let plot = response.plot;
                    let imageSrc = 'data:image/png;base64,' + plot;
                    $('#xyz-plot-image').attr('src', imageSrc);

                    let std_values = response.std_values;
                    let x = parseFloat(std_values['x'].toFixed(2))
                    let y = parseFloat(std_values['y'].toFixed(2))
                    let z = parseFloat(std_values['z'].toFixed(2))

                    let warning = $('#xyz-warning')
                    if (z > 0.2 && y > 0.2) {
                        warning.html('Warning! Possible asthma attack!')
                        warning.css('color', 'red');
                        warning.css('font-weight', 'bold');
                    } else {
                        warning.html('Breath seems to be normal')
                        warning.css('color', 'green');  // Change the text color to red
                    }

                }
            });
        }
        setInterval(updateXYZPlot, 100);

function updateSpO2Plot() {
            $.ajax({
                url: '/get_spO2_plot',
                success: function(response) {
                    let plot = response.plot;
                    let imageSrc = 'data:image/png;base64,' + plot;
                    $('#spO2-plot-image').attr('src', imageSrc);

                    let data = response.data;
                    let healthy = data['healthy']
                    let measured = data['measured']
                    let std = data['std']
                    let error = data['error']
                    let warning = $('#spO2-warning')
                    console.log(data)

                    if (error) {
                        warning.html('Warning! SpO2 level couldn\'t be measured!')
                        warning.css('color', 'red');
                        warning.css('font-weight', 'bold');
                    } else if (healthy < measured + std) {
                        warning.html('SpO2 level is OK')
                        warning.css('color', 'green');  // Change the text color to red
                    } else {
                        warning.html('Warning! SpO2 level is too low!')
                        warning.css('color', 'red');
                        warning.css('font-weight', 'bold');
                    }
                }
            });
        }
        setInterval(updateSpO2Plot, 4000);

function updateTempPlot() {
            $.ajax({
                url: '/get_temp_plot',
                success: function(response) {
                    let plot = response.plot;
                    let imageSrc = 'data:image/png;base64,' + plot;
                    $('#temp-plot-image').attr('src', imageSrc);

                    let data = response.data;
                    let warning = $('#temp-warning')
                    let diff = data['healthy'] - data['measured']

                    if (diff > 1) {
                        warning.html('Warning! Temperature too low')
                        warning.css('color', 'red');
                        warning.css('font-weight', 'bold');
                    } else if(diff < -1) {
                        warning.html('Warning! Temperature too high')
                        warning.css('color', 'red');
                        warning.css('font-weight', 'bold');
                    }
                    else {
                        warning.html('Temperature is OK')
                        warning.css('color', 'green');
                    }


                }
            });
        }
        setInterval(updateTempPlot, 4000);