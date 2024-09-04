
    let labelColor, headingColor, borderColor, legendColor;
  
      labelColor = config.colors_dark.textMuted;
      headingColor = config.colors_dark.headingColor;
      borderColor = config.colors_dark.borderColor;
      legendColor = config.colors_dark.bodyColor;
  
    // Chart Colors
    const chartColors = {
      donut: {
        series1: '#5AB12C',
        series2: '#66C732',
        series3: '#8DE45F',
        series4: '#C6F1AF'
      },
      line: {
        series1: config.colors.warning,
        series2: config.colors.primary,
        series3: '#7367f029'
      }
    };
  
    // chart_painel_contas_a_pagar
    // --------------------------------------------------------------------
    const shipmentEl = document.querySelector('#chart_painel_contas_a_pagar'),
      shipmentConfig = {
        series: [
          {
            name: 'Pendentes',
            type: 'column',
            data: [38, 45, 33, 38, 32, 50, 48, 40, 42, 37]
          },
          {
            name: 'Pagos',
            type: 'line',
            data: [23, 28, 23, 32, 28, 44, 32, 38, 26, 34]
          }
        ],
        chart: {
          height: 320,
          type: 'line',
          stacked: false,
          parentHeightOffset: 0,
          toolbar: { show: false },
          zoom: { enabled: false }
        },
        markers: {
          size: 5,
          colors: [config.colors.white],
          strokeColors: chartColors.line.series2,
          hover: { size: 6 },
          borderRadius: 4
        },
        stroke: {
          curve: 'smooth',
          width: [0, 3],
          lineCap: 'round'
        },
        legend: {
          show: true,
          position: 'bottom',
          markers: {
            width: 8,
            height: 8,
            offsetX: -3
          },
          height: 40,
          itemMargin: {
            horizontal: 10,
            vertical: 0
          },
          fontSize: '15px',
          fontFamily: 'Public Sans',
          fontWeight: 400,
          labels: {
            colors: headingColor,
            useSeriesColors: false
          },
          offsetY: 10
        },
        grid: {
          strokeDashArray: 8,
          borderColor
        },
        colors: [chartColors.line.series1, chartColors.line.series2],
        fill: {
          opacity: [1, 1]
        },
        plotOptions: {
          bar: {
            columnWidth: '30%',
            startingShape: 'rounded',
            endingShape: 'rounded',
            borderRadius: 4
          }
        },
        dataLabels: { enabled: false },
        xaxis: {
          tickAmount: 10,
          categories: ['1 Jan', '2 Jan', '3 Jan', '4 Jan', '5 Jan', '6 Jan', '7 Jan', '8 Jan', '9 Jan', '10 Jan'],
          labels: {
            style: {
              colors: labelColor,
              fontSize: '13px',
              fontFamily: 'Public Sans',
              fontWeight: 400
            }
          },
          axisBorder: { show: false },
          axisTicks: { show: false }
        },
        yaxis: {
          tickAmount: 4,
          min: 0,
          max: 50,
          labels: {
            style: {
              colors: labelColor,
              fontSize: '13px',
              fontFamily: 'Public Sans',
              fontWeight: 400
            },
            formatter: function (val) {
              return val + '%';
            }
          }
        },
        responsive: [
          {
            breakpoint: 1400,
            options: {
              chart: { height: 320 },
              xaxis: { labels: { style: { fontSize: '10px' } } },
              legend: {
                itemMargin: {
                  vertical: 0,
                  horizontal: 10
                },
                fontSize: '13px',
                offsetY: 12
              }
            }
          },
          {
            breakpoint: 1025,
            options: {
              chart: { height: 415 },
              plotOptions: { bar: { columnWidth: '50%' } }
            }
          },
          {
            breakpoint: 982,
            options: { plotOptions: { bar: { columnWidth: '30%' } } }
          },
          {
            breakpoint: 480,
            options: {
              chart: { height: 250 },
              legend: { offsetY: 7 }
            }
          }
        ]
      };
    if (typeof shipmentEl !== undefined && shipmentEl !== null) {
      const shipment = new ApexCharts(shipmentEl, shipmentConfig);
      shipment.render();
    }
