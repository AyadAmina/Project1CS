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
              backgroundColor: ['rgba(38, 70, 83, 0.3)','rgba(38, 70, 83, 0.6)', 'rgba(38, 70, 83, 0.9)', 'rgba(233, 196, 106,.4)', 'rgba(233, 196, 106,.6)', 'rgba(233, 196, 106,.9)',
                  
                 ] // Sample colors
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
          backgroundColor: ['#2a9d8f', 'rgb(233, 196, 106)', 'rgba(38, 70, 83, 0.9)', 'rgba(38, 70, 83, 0.5)', 'rgba(42, 157, 143,.6)']
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
          backgroundColor: ['#2a9d8f', 'rgb(233, 196, 106)', 'rgba(38, 70, 83, 0.9)', 'rgba(38, 70, 83, 0.5)', 'rgba(42, 157, 143,.6)']
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
          backgroundColor: ['#2a9d8f', 'rgb(233, 196, 106)', 'rgba(38, 70, 83, 0.9)', 'rgba(38, 70, 83, 0.5)', 'rgba(42, 157, 143,.6)']
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