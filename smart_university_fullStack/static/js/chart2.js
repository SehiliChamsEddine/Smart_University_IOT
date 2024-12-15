// ---------- CHARTS ----------

// Define the chart options
let options = {
    chart: {
      type: 'area',
      height: 350,
      animations: {
        enabled: true,
        easing: 'linear',
        dynamicAnimation: {
          speed: 1000
        }
      },
      foreColor: '#00E396' // Change color of axes to white
    },
    series: [{
      data: [],
      fill: {
        type: 'gradient',
        gradient: {
          shadeIntensity: 1,
          opacityFrom: 0.7,
          opacityTo: 0.9,
          stops: [0, 12]
        }
      }
    }],
    xaxis: {
      type: 'datetime',
      range: 10000
    },
    yaxis: {
      decimalsInFloat: 0,
      max: 12
    },
    stroke: {
      curve: 'smooth'
    },
  };
  
  // --------------------------------------------
  // Create the chart
  let chart = new ApexCharts(document.querySelector("#line-chart"), options);
  chart.render();
  
  // Define the chart options
  let options1 = {
    chart: {
      type: 'area',
      height: 350,
      animations: {
        enabled: true,
        easing: 'linear',
        dynamicAnimation: {
          speed: 1000
        }
      },
      foreColor: '#00E396' // Change color of axes to white
    },
    series: [{
      data: [],
      fill: {
        type: 'gradient',
        gradient: {
          shadeIntensity: 1,
          opacityFrom: 0.7,
          opacityTo: 0.9,
          stops: [0, 12]
        }
      }
    }],
    xaxis: {
      type: 'datetime',
      range: 10000
    },
    yaxis: {
      decimalsInFloat: 0,
      max: 12
    },
    stroke: {
      curve: 'smooth'
    },
  };
  
  // Create the chart
  let chart1 = new ApexCharts(document.querySelector("#line-charts"), options1);
  chart1.render();
  
  // Function to fetch the latest voltage data
  function fetchLatestVoltageData() {
    fetch('/get_latest_voltage/')
      .then(response => response.json())
      .then(data => {
        let x = new Date(data.timestamp).getTime(),
            y = data.voltage;
  
        let color = (y > 6) ? '#FF0000' : '#00E396'; // Red if y > 6, otherwise green
  
        // Update color for the entire series
        chart.updateOptions({
          series: [{
            fill: {
              color: color
            }
          }]
        });
  
        // Append new data point
        chart.appendData({
          data: [{
            x: x,
            y: y
          }]
        });
  
        color = (y > 5) ? '#FF0000' : '#080808'; // Red if y > 5, otherwise green
  
        // Update color for the entire series
        chart1.updateOptions({
          series: [{
            fill: {
              color: color
            }
          }]
        });
  
        // Append new data point
        chart1.appendData({
          data: [{
            x: x,
            y: y
          }]
        });
      })
      .catch(error => console.error('Error:', error));
  }
  
  // Update the chart with real-time data
  window.setInterval(fetchLatestVoltageData, 1000);
  