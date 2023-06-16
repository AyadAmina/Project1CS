// Assuming you have included the Chart.js library

// Function to create the pie chart
function createPieChart(chartData) {
  // Pie chart configuration
  var chartConfig = {
      type: 'pie',
      data: {
          labels: chartData.labels,
          datasets: [{
              data: chartData.values,
              backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', 'rgba(0, 171, 197, .9)',
                  'rgba(0, 171, 197, .7)',
                  'rgba(0, 171, 197, .5)'] // Sample colors
          }]
      },
      options: {
          responsive: true,
          maintainAspectRatio: false
      }
  };

  // Create the pie chart
  var pieChart = new Chart(document.getElementById('pie-chart'), chartConfig);
}

// Create the pie chart using the fetched data
createPieChart(chartData);
