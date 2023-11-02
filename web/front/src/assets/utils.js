const secondsToDhms = (seconds) => {
    seconds = Number(seconds);

    if (seconds == 0)
        return '0'

    var d = Math.floor(seconds / (3600 * 24));
    var h = Math.floor(seconds % (3600 * 24) / 3600);
    var m = Math.floor(seconds % 3600 / 60);
    var s = Math.floor(seconds % 60);

    var dDisplay = d > 0 ? d + (d == 1 ? " dia " : " dias ") : "";
    var hDisplay = h > 0 ? h + (h == 1 ? " h " : " hs ") : "";
    var mDisplay = m > 0 ? m + (m == 1 ? " m " : " mins ") : "";
    var sDisplay = s > 0 ? s + (s == 1 ? " s" : " segs") : "";
    return dDisplay + hDisplay + mDisplay + sDisplay;
}

function formatBytes(bytes, decimalPoint=2) {
    if(bytes == 0) return '0 Bytes';
    var k = 1000,
        dm = decimalPoint || 2,
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function formatNumbers(val, decimalPoint=1) {
    if(val == 0) return '-';
    var k = 1000,
        dm = decimalPoint || 2,
        sizes = ['', 'K', 'M', 'M', 'M', 'M', 'M', 'M', 'M'],
        i = Math.floor(Math.log(val) / Math.log(k));
    return parseFloat((val / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
 }

const getChartData = (values, label) => {
    return [
        {
            name: label,
            data: values
        }
    ]
}

const getChartOptions = (labels, _id) => {
    return {
        chart: {
            id: _id,
            toolbar: {
                show: false,
            },
            dropShadow: {
                enabled: true,
                top: 13,
                left: 0,
                blur: 10,
                opacity: 0.1,
                color: "#4318FF",
            },
        },
        colors: ["#4318FF", "#39B8FF"],
        markers: {
            size: 0,
            colors: "white",
            strokeColors: "#7551FF",
            strokeWidth: 3,
            strokeOpacity: 0.9,
            strokeDashArray: 0,
            fillOpacity: 1,
            discrete: [],
            shape: "circle",
            radius: 2,
            offsetX: 0,
            offsetY: 0,
            showNullDataPoints: true,
        },
        tooltip: {
            theme: "dark",
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: "smooth",
            type: "line",
        },
        xaxis: {
            type: "numeric",
            categories: labels,
            labels: {
                style: {
                    colors: "#A3AED0",
                    fontSize: "12px",
                    fontWeight: "500",
                },
            },
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
        },
        yaxis: {
            show: false,
        },
        legend: {
            show: false,
        },
        grid: {
            show: false,
            column: {
                color: ["#7551FF", "#39B8FF"],
                opacity: 0.5,
            },
        },
        color: ["#7551FF", "#39B8FF"],
    }
}

const getPieChartOptions = (labels, formatter = null) => {
    return {
        labels: labels,
        chart: {
          width: "550px"
        },
        states: {
          hover: {
            filter: {
              type: "none",
            },
          },
        },
        legend: {
          show: false,
        },
        dataLabels: {
          enabled: false,
        },
        hover: { mode: null },
        plotOptions: {
          donut: {
            expandOnClick: false,
            donut: {
              labels: {
                show: false,
              },
            },
          },
        },
        tooltip: {
          enabled: true,
          theme: "dark",
          y: {
              formatter: formatter
          }
        },
    };
};

export {
    secondsToDhms,
    getChartData,
    getChartOptions,
    getPieChartOptions,
    formatBytes,
    formatNumbers
}