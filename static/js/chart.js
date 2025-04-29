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

    // ✅ CountUp.js integration
    const countTarget = document.getElementById("debt-count");
    
    if (countTarget) {
      const rawDebt = parseFloat(countTarget.textContent.replace(/[^0-9.-]+/g, ""));
      const counter = new countUp.CountUp("debt-count", rawDebt, {
        duration: 3,
        separator: ",",
        decimal: "."
      });
      
    
      if (!counter.error) {
        counter.start();
      } else {
        console.error("❌ CountUp error:", counter.error);
      }
    } else {
      console.error("❌ Could not find #debt-count in the DOM");
    }

    // countdown target

    const countdownTarget = document.getElementById("countdown-debt");

    if (countdownTarget) {
      const rawCountdown = parseFloat(countdownTarget.textContent.replace(/[^0-9.-]+/g, ""));
      const countdownCounter = new countUp.CountUp("countdown-debt", rawCountdown, {
        startVal: 2_000_000_000_000,
        duration: 3,
        separator: ",",
        decimal: "."
      });

      if (!countdownCounter.error) {
        countdownCounter.start();
      } else {
        console.error("❌ Countdown CountUp error:", countdownCounter.error);
      }
    }

    
    

  });
  