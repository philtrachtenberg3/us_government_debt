document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("debtChart").getContext("2d");
  
    const chartDates = JSON.parse(document.getElementById("chartDates").textContent);
    const chartValues = JSON.parse(document.getElementById("chartValues").textContent);
  
    new Chart(ctx, {
      type: "line",
      data: {
        labels: chartDates,
        datasets: [
          {
            label: "Total Public Debt Outstanding ($)",
            data: chartValues,
            fill: true,
            tension: 0.2,
            borderWidth: 2,
            pointRadius: 0,
          },
        ],
      },
      options: {
        scales: {
          x: {
            ticks: { maxTicksLimit: 10 },
            title: { display: true, text: "Date" }
          },
          y: {
            title: { display: true, text: "Debt ($)" },
            min: 0,
          }
        },
        plugins: {
          legend: { display: false }
        },
        responsive: true,
        maintainAspectRatio: false
      }      
    });
  });
  