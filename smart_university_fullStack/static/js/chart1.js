// ---------- CHARTS ----------

let chart_color1 = "#00E396";
let chart_color2 = "#00E396";
// Define the chart options
let options = {
  chart: {
    type: "area",
    height: 350,
    animations: {
      enabled: true,
      easing: "linear",
      dynamicAnimation: {
        speed: 1000,
      },
    },
    foreColor: "#00E396", // Change color of axes to white
  },
  series: [
    {
      data: [],
      color: "#00E396", // Change color of line to green
      fill: {
        type: "gradient",
        gradient: {
          shadeIntensity: 1,
          opacityFrom: 0.7,
          opacityTo: 0.9,
          stops: [0, 100],
        },
      },
    },
  ],
  xaxis: {
    type: "datetime",
    range: 20000,
  },
  yaxis: {
    decimalsInFloat: 0,

    max: 100,
  },
  stroke: {
    curve: "smooth",
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
    type: "area",
    height: 350,
    animations: {
      enabled: true,
      easing: "linear",
      dynamicAnimation: {
        speed: 1000,
      },
    },
    foreColor: "#00E396", // Change color of axes to white
  },
  series: [
    {
      data: [],
      color: "#00E396", // Change color of line to green
      fill: {
        type: "gradient",
        gradient: {
          shadeIntensity: 0.5,
          opacityFrom: 0.7,
          opacityTo: 0.9,
          stops: [0, 100],
        },
      },
    },
  ],
  xaxis: {
    type: "datetime",
    range: 20000,
  },
  yaxis: {
    // forceNiceScale: true,
    decimalsInFloat: 0,
    max: 100,
  },
  stroke: {
    curve: "smooth",
  },
};

// --------------------------------------------
// Create the chart
let chart1 = new ApexCharts(document.querySelector("#line-chart1"), options1);
chart1.render();

// -----------------------------------------------------------------------------------
// ------------------------------------------------------------------------------

// Define the chart options
let options2 = {
  chart: {
    type: "area",
    height: 350,
    animations: {
      enabled: true,
      easing: "linear",
      dynamicAnimation: {
        speed: 1000,
      },
    },
    foreColor: "#00E396", // Change color of axes to white
  },
  series: [
    {
      data: [],
      color: "#00E396", // Change color of line to green
      fill: {
        type: "gradient",
        gradient: {
          shadeIntensity: 0.5,
          opacityFrom: 0.7,
          opacityTo: 0.9,
          stops: [0, 100],
        },
      },
    },
  ],
  xaxis: {
    type: "datetime",
    range: 20000,
  },
  yaxis: {
    // forceNiceScale: true,
    decimalsInFloat: 0,
    max: 100,
  },
  stroke: {
    curve: "smooth",
  },
};

// --------------------------------------------
// Create the chart
let chart2 = new ApexCharts(document.querySelector("#line-chart2"), options2);
chart2.render();
//  // Function to fetch the latest voltage data

function fetchLatestVoltageData() {
  fetch("/get_latest_data/")
    .then((response) => response.json())
    .then((data) => {
      let x1 = new Date(data.timestamp_tempurature).getTime(),
        y1 = data.tempurature;
      let x2 = new Date(data.timestamp_himidity).getTime(),
        y2 = data.himidity;
      let x3 = new Date(data.timestamp_waterlevel).getTime(),
        y3 = data.waterlevel;
      console.log(data);
      chart.appendData([
        {
          data: [
            {
              x: x1,
              y: y1,
            },
          ],
        },
      ]);
      // Assuming you have another chart called chart1
      chart1.appendData([
        {
          data: [
            {
              x: x2,
              y: y2,
            },
          ],
        },
      ]);
      chart2.appendData([
        {
          data: [
            {
              x: x3,
              y: y3,
            },
          ],
        },
      ]);
    })
    .catch((error) => console.error("Error:", error));
}

// Update the chart with real-time data
window.setInterval(fetchLatestVoltageData, 1000);
