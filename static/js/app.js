loadAnalytics();

async function loadAnalytics() {
  const res = await fetch("/analytics/summary");
  const data = await res.json();

  // Total predictions
  const totalEl = document.getElementById("total_predictions");
  if (totalEl) {
    totalEl.innerText = data.total_predictions;
  }

  // Top locations
  const locList = document.getElementById("top_locations");
  if (locList) {
    locList.innerHTML = "";
    data.top_locations.forEach(item => {
      const li = document.createElement("li");
      li.innerText = `${item.location} — ${item.count}`;
      locList.appendChild(li);
    });
  }

  // Avg price by BHK
  const bhkList = document.getElementById("avg_price_bhk");
  if (bhkList) {
    bhkList.innerHTML = "";
    data.avg_price_by_bhk.forEach(item => {
      const li = document.createElement("li");
      li.innerText = `${item.bhk} BHK → ₹${item.avg_price} Lakhs`;
      bhkList.appendChild(li);
    });
  }
}
async function loadLocations() {
  const res = await fetch("/locations");
  const locations = await res.json();

  const select = document.getElementById("location");
  select.innerHTML = "";

  locations.forEach(loc => {
    const opt = document.createElement("option");
    opt.value = loc;
    opt.textContent = loc;
    select.appendChild(opt);
  });
}

document.addEventListener("DOMContentLoaded", loadLocations);
