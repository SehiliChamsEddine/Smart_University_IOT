// SIDEBAR TOGGLE

var sidebarOpen = false;
var sidebar = document.getElementById('sidebar');

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add('sidebar-responsive');
    sidebar.classList.add("sidebar-open");
    sidebar.classList.remove("sidebar-closed");
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove('sidebar-responsive');
    sidebar.classList.remove("sidebar-open");
    sidebar.classList.add("sidebar-closed");
    sidebarOpen = false;
  }
}

// ---------- CHARTS ----------


 
// Define the chart options
let options = {
  chart: {
    type: 'line',
    height: 350,
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: {
        speed: 1000
      }
    },
    foreColor: '#FFFFFF' // Change color of axes to white
  },
  series: [{
    data: [],
    color: '#00E396', // Change color of line to green
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

// ------------------------------------------------------------------------------

// Define the chart options
let options1 = {
  chart: {
    type: 'line',
    height: 350,
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: {
        speed: 1000
      }
    },
    foreColor: '#FFFFFF' // Change color of axes to white
  },
  series: [{
    data: [],
    color: '#00E396', // Change color of line to green
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
    // forceNiceScale: true,
    decimalsInFloat: 0 ,
    max: 12
  },
  stroke: {
    curve: 'smooth'
  },
};




// --------------------------------------------
// Create the chart
let chart1 = new ApexCharts(document.querySelector("#line-charts"), options1);
chart1.render();



// -----------------------------------------------------------------------------------

// Function to fetch the latest voltage data
function fetchLatestVoltageData() {
  fetch('/get_latest_voltage/')
    .then(response => response.json())
    .then(data => {
      let x = new Date(data.timestamp).getTime(),
          y = data.voltage;

      chart.appendData([{
        data: [{
          x: x,
          y: y
        }]
      }]);
      // Assuming you have another chart called chart1
      chart1.appendData([{
        data: [{
          x: x,
          y: y
        }]
      }]);
    })
    .catch(error => console.error('Error:', error));
}

// Update the chart with real-time data
window.setInterval(fetchLatestVoltageData, 1000);
