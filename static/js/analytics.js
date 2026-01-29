document.addEventListener("DOMContentLoaded", loadAnalytics);

async function loadAnalytics() {
  const res = await fetch("/analytics/summary");
  const data = await res.json();

  document.getElementById("total_predictions").innerText =
    data.total_predictions;

  const locList = document.getElementById("top_locations");
  locList.innerHTML = "";
  data.top_locations.forEach(item => {
    const li = document.createElement("li");
    li.innerText = `${item.location} — ${item.count}`;
    locList.appendChild(li);
  });

  const bhkList = document.getElementById("avg_price_bhk");
  bhkList.innerHTML = "";
  data.avg_price_by_bhk.forEach(item => {
    const li = document.createElement("li");
    li.innerText = `${item.bhk} BHK → ₹${item.avg_price} Lakhs`;
    bhkList.appendChild(li);
  });
}
