document.addEventListener("DOMContentLoaded", async function() {
  await loadLocations();
  await loadHistory();
});

async function loadLocations() {
  try {
    const res = await fetch("/locations");
    const locations = await res.json();

    const dropdown = document.getElementById("location");
    dropdown.innerHTML = "";

    locations.forEach(loc => {
      const option = document.createElement("option");
      option.value = loc;
      option.text = loc;
      dropdown.appendChild(option);
    });
  } catch (e) {
    console.error("Failed to load locations:", e);
  }
}

async function predict() {
  document.getElementById("result").innerText = "";
  document.getElementById("context").innerText = "";

  const payload = {
    area_sqft: parseFloat(document.getElementById("area").value),
    bhk: parseInt(document.getElementById("bhk").value),
    bath: parseInt(document.getElementById("bath").value),
    location: document.getElementById("location").value
  };

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    console.log(data);

    if (!data.success) {
      document.getElementById("context").innerText = `❌ Error: ${data.error}`;
      return;
    }

    document.getElementById("result").innerText =
      `₹${data.predicted_price_lakhs} Lakhs`;

    document.getElementById("context").innerText =
      `🌤 Temperature: ${data.weather.temperature}°C | Metro Distance: ${data.weather.metro_distance} km`;

    loadHistory();
  } catch (e) {
    document.getElementById("context").innerText = `❌ Network error: ${e.message}`;
  }
}

async function loadHistory() {
  try {
    const res = await fetch("/predictions");
    const data = await res.json();

    const list = document.getElementById("history");
    list.innerHTML = "";

    data.forEach(item => {
      if (item.area_sqft && item.location && item.predicted_price !== undefined) {
        const li = document.createElement("li");
        li.innerText =
          `${item.area_sqft} sqft | ${item.location} → ₹${item.predicted_price} Lakhs`;
        list.appendChild(li);
      }
    });
  } catch (e) {
    console.error("Failed to load history:", e);
  }
}
