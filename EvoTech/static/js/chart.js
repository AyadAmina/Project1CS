// Assuming you have included the Chart.js library

// Function to create the pie chart
function createPieChart(chartData) {
  // Pie chart configuration
  var chartConfig = {
      type: 'pie',
      data: {
          labels: chartData.cotes,
          datasets: [{
              data: chartData.cote_feedback,
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



function createBarChart(chartData) {
    // Bar chart configuration
    var chartConfig = {
      type: 'bar',
      data: {
        labels: chartData.lieu_names,
        datasets: [{
          label: 'Feedback',
          data: chartData.feedback_values,
          backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#cc65fe', '#ff9800']
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            grid: {
              display: false
            }
          },
          y: {
            grid: {
              display: true
            },
            beginAtZero: true
          }
        }
      }
    };

    // Create the bar chart
    var barChart = new Chart(document.getElementById('bar-chart'), chartConfig);
  }


function createPolarChart(chartData) {
    // Bar chart configuration
    var chartConfig = {
      type: 'polarArea',
      data: {
        labels: chartData.region_names,
        datasets: [{
          data: chartData.event_counts,
          backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#cc65fe', '#ff9800']
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    };

    // Create the bar chart
    var polarChart = new Chart(document.getElementById('polar-chart'), chartConfig);
  }


  function createBarChart2(chartData) {
    // Bar chart configuration
    var chartConfig = {
      type: 'bar',
      data: {
        labels: chartData.lieu_favoris,
        datasets: [{
          label: 'Feedback',
          data: chartData.favorites_counts,
          backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#cc65fe', '#ff9800']
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            grid: {
              display: false
            }
          },
          y: {
            grid: {
              display: true
            },
            beginAtZero: true
          }
        }
      }
    };

    // Create the bar chart
    var barChart = new Chart(document.getElementById('bar-chart2'), chartConfig);
  }