function updateXYZ() {
            $.ajax({
                url: '/get_xyz',
                success: function(response) {
                    var values = response.values;

                    var valueTable = $('#xyz-table');
                    var valueBody = $('#xyz-body');
                    valueBody.empty();  // Clear the existing table body

                    // Iterate over the values array and generate rows
                    values.forEach(function(row) {
                        var newRow = $('<tr>');
                        row.forEach(function(value) {
                            var newCell = $('<td>').text(value);
                            newRow.append(newCell);
                        });
                        valueBody.append(newRow);
                    });

                    // Scroll to the bottom of the table
                    valueTable.scrollTop(valueTable.prop("scrollHeight"));
                }
            });
        }
        setInterval(updateXYZ, 100);

function updateMAX() {
            $.ajax({
                url: '/get_max',
                success: function(response) {
                    var values = response.values;

                    var valueTable = $('#max-table');
                    var valueBody = $('#max-body');
                    valueBody.empty();  // Clear the existing table body

                    // Iterate over the values array and generate rows
                    values.forEach(function(row) {
                        var newRow = $('<tr>');
                        row.forEach(function(value) {
                            var newCell = $('<td>').text(value);
                            newRow.append(newCell);
                        });
                        valueBody.append(newRow);
                    });

                    // Scroll to the bottom of the table
                    valueTable.scrollTop(valueTable.prop("scrollHeight"));
                }
            });
        }
        setInterval(updateMAX, 1000);

function updateXPlot() {
            $.ajax({
                url: '/get_xyz_plot',
                success: function(response) {
                    var plot = response.plot;

                    // Convert the base64-encoded plot to an image source
                    var imageSrc = 'data:image/png;base64,' + plot;

                    // Update the plot image on the page
                    $('#plot-image').attr('src', imageSrc);

                }
            });
        }
        setInterval(updateXPlot, 100);