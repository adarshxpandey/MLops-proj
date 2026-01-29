document.addEventListener("DOMContentLoaded", async function() {
  await loadAnalytics();
});

async function loadAnalytics() {
  const errorDiv = document.getElementById("analytics-error");
  
  try {
    const res = await fetch("/analytics/summary");
    const data = await res.json();
    console.log(data);

    // Populate totals
    document.getElementById("total-predictions").innerHTML = data.total_predictions;

    // Populate top locations
    const topLocsList = document.getElementById("top-locations");
    topLocsList.innerHTML = "";
    
    if (data.top_locations.length === 0) {
      topLocsList.innerHTML = "<li class='loading'>No data yet</li>";
    } else {
      data.top_locations.forEach(item => {
        const li = document.createElement("li");
        li.innerText = `${item.location}: ${item.count} predictions`;
        topLocsList.appendChild(li);
      });
    }

    // Populate avg by BHK
    const avgBhkList = document.getElementById("avg-by-bhk");
    avgBhkList.innerHTML = "";
    
    if (data.avg_price_by_bhk.length === 0) {
      avgBhkList.innerHTML = "<li class='loading'>No data yet</li>";
    } else {
      data.avg_price_by_bhk.forEach(item => {
        const li = document.createElement("li");
        li.innerText = `${item.bhk} BHK: ₹${item.avg_price} Lakhs avg`;
        avgBhkList.appendChild(li);
      });
    }
  } catch (e) {
    console.error("Failed to load analytics:", e);
    errorDiv.style.display = "block";
    errorDiv.innerText = `❌ Error: ${e.message}`;
  }
}

/* -----------------------------
   Average Price by BHK Chart
----------------------------- */
const bhkLabels = data.avg_price_by_bhk.map(
  item => `${item.bhk} BHK`
);
const bhkPrices = data.avg_price_by_bhk.map(
  item => item.avg_price
);

new Chart(document.getElementById("bhkChart"), {
  type: "bar",
  data: {
    labels: bhkLabels,
    datasets: [
      {
        label: "Avg Price (₹ Lakhs)",
        data: bhkPrices,
        borderWidth: 1
      }
    ]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
