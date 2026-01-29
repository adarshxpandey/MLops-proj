document.addEventListener("DOMContentLoaded", () => {
  loadLocations();
  loadHistory();
});

async function loadLocations() {
  const res = await fetch("/locations");
  const locations = await res.json();

  const select = document.getElementById("location");
  if (!select) return;

  select.innerHTML = "";

  locations.forEach(loc => {
    const opt = document.createElement("option");
    opt.value = loc;
    opt.textContent = loc;
    select.appendChild(opt);
  });
}

async function predict() {
  const payload = {
    area_sqft: Number(document.getElementById("area").value),
    bhk: Number(document.getElementById("bhk").value),
    bath: Number(document.getElementById("bath").value),
    location: document.getElementById("location").value
  };

  const res = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  document.getElementById("result").innerText =
    `₹${data.predicted_price_lakhs} Lakhs`;

  document.getElementById("weather").innerHTML = `
    🌡 Temp: ${data.weather.temperature}°C<br>
    🚇 Metro Distance: ${data.weather.metro_distance} km<br>
    🌧 Raining: ${data.weather.is_raining ? "Yes" : "No"}
  `;

  loadHistory();
}

async function loadHistory() {
  const res = await fetch("/predictions");
  const data = await res.json();

  const list = document.getElementById("history");
  if (!list) return;

  list.innerHTML = "";

  data.slice(0, 10).forEach(item => {
    const li = document.createElement("li");
    li.innerText = `${item.area_sqft} sqft | ${item.location} → ₹${item.predicted_price} Lakhs`;
    list.appendChild(li);
  });
}
