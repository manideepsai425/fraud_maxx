async function predict() {

    let amount = parseFloat(document.getElementById("amount").value);
    let time = parseFloat(document.getElementById("time").value);
    let locationSelect = document.getElementById("location");
    let locationCode = locationSelect.value;
    let locationName = locationSelect.options[locationSelect.selectedIndex]?.text || locationCode;
    let deviceSelect = document.getElementById("device");
    let deviceCode = deviceSelect.value;
    let deviceName = deviceSelect.options[deviceSelect.selectedIndex]?.text || deviceCode;

    // Map location code to numeric feature value for the model
    // Normal/unusual are special flags; all other country codes map to 1.
    const locationMap = {
        normal: 0,
        unusual: 3
    };

    const deviceMap = {
        known: 0,
        new: 3,
        android_phone: 1,
        ios_phone: 1,
        windows_pc: 1,
        mac_desktop: 1,
        linux_pc: 1,
        tablet: 1,
        smart_tv: 2,
        pos_terminal: 0,
        vpn: 3,
        bot: 3
    };

    let location = locationMap[locationCode] ?? 1;
    let device = deviceMap[deviceCode] ?? 1;

    let features = new Array(29).fill(0);

    features[0] = amount;
    features[1] = time;
    features[2] = location;
    features[3] = device;

    let response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ features: features })
    });

    let data = await response.json();

    let resultDiv = document.getElementById("result");

    resultDiv.innerHTML = `
        <h3 style="color:${data.prediction === 1 ? 'red' : 'lightgreen'}">
            ${data.prediction === 1 ? "⚠ Fraud Detected" : "✅ Safe Transaction"}
        </h3>
        <p><strong>Location selected:</strong> ${locationName} (${locationCode})</p>
        <p><strong>Device selected:</strong> ${deviceName} (${deviceCode})</p>
        <p>Probability: ${(data.probability * 100).toFixed(2)}%</p>
        <p>Reasons:</p>
        <ul>
            ${data.explanation.map(e => `<li>${e}</li>`).join("")}
        </ul>
    `;
}