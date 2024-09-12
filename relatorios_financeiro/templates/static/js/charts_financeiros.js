// Ranking Bancos
function gera_grafico_rank_bancos(array_nomes, array_percents, cores, percent_max){

const coresParaGrafico = array_nomes.map(banco => cores[banco] || 'defaultColor');

const horizontalRankBancos = document.querySelector('#horizontalbancos'),
    horizontalBarChartConfig = {
      chart: {
        height: 300,
        type: 'bar',
        toolbar: {
          show: false
        }
      },
      plotOptions: {
        bar: {
          horizontal: true,
          barHeight: '70%',
          distributed: true,
          startingShape: 'rounded',
          borderRadius: 7
        }
      },
      grid: {
        strokeDashArray: 10,
        borderColor: config.colors_dark.borderColor,
        xaxis: {
          lines: {
            show: true
          }
        },
        yaxis: {
          lines: {
            show: false
          }
        },
        padding: {
          top: -35,
          bottom: -12
        }
      },

      colors: coresParaGrafico,
      /*colors: [
        config.colors.primary,
        config.colors.info,
        config.colors.success,
        config.colors.secondary,
        config.colors.danger,
        config.colors.warning
      ],
      */
      fill: {
        opacity: [1, 1, 1, 1, 1, 1]
      },
      dataLabels: {
        enabled: true,
        style: {
          colors: ['#fff'],
          fontWeight: 400,
          fontSize: '13px',
          fontFamily: 'Public Sans'
        },
        formatter: function (val, opts) {
          return horizontalBarChartConfig.labels[opts.dataPointIndex];
        },
        offsetX: 0,
        dropShadow: {
          enabled: false
        }
      },
      labels: array_nomes,
      series: [
        {
          data: array_percents
        }
      ],

      xaxis: {
        categories: ['1', '2', '3', '4', '5', '6'],
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
        labels: {
          style: {
            colors: config.colors_dark.borderColor,
            fontFamily: 'Public Sans',
            fontSize: '13px'
          },
          formatter: function (val) {
            return `${Math.round(val)}%`;
          }
        }
      },
      yaxis: {
        max: percent_max,
        labels: {
          style: {
            colors: [config.colors_dark.borderColor],
            fontFamily: 'Public Sans',
            fontSize: '13px'
          }
        }
      },
      tooltip: {
        enabled: true,
        style: {
          fontSize: '12px'
        },
        onDatasetHover: {
          highlightDataSeries: false
        },
        custom: function ({ series, seriesIndex, dataPointIndex, w }) {
          return '<div class="px-3 py-2">' + '<span>' + series[seriesIndex][dataPointIndex] + '%</span>' + '</div>';
        }
      },
      legend: {
        show: false
      }
    };
  if (typeof horizontalRankBancos !== undefined && horizontalRankBancos !== null) {
    const horizontalBarChart = new ApexCharts(horizontalRankBancos, horizontalBarChartConfig);
    horizontalBarChart.render();
  }

  
  // Total Clientes Nexxera
  const expensesRadialChartEl = document.querySelector('#clientes_nexxera'),
    expensesRadialChartConfig = {
      chart: {
        height: 400,
        sparkline: {
          enabled: true
        },
        parentHeightOffset: 0,
        type: 'radialBar'
      },
      colors: [config.colors.primary],
      series: [porcentagem_nexxera],
      plotOptions: {
        radialBar: {
          startAngle: -90,
          endAngle: 90,
          hollow: {
            size: '55%'
          },
          track: {
            background: config.colors_label.secondary
          },
          dataLabels: {
            name: {
              show: false
            },
            value: {
              fontSize: '50px',
              fontFamily: 'Public Sans',
              color: "#000",
              fontWeight: 500,
              offsetY: -5
            }
          }
        }
      },
      grid: {
        show: false,
        padding: {
          left: -10,
          right: -10,
          bottom: 5
        }
      },
      stroke: {
        lineCap: 'round'
      },
      labels: ['Progress']
    };

  if (typeof expensesRadialChartEl !== undefined && expensesRadialChartEl !== null) {
    const expensesRadialChart = new ApexCharts(expensesRadialChartEl, expensesRadialChartConfig);
    expensesRadialChart.render();
  }
}