/* =========================================
   UrbanFlow Dashboard - Live AI Integration
========================================= */

// =========================================
// HTML ELEMENTS
// =========================================
const timer = document.getElementById("timer");
const elapsedElement = document.getElementById("elapsed");
const remainingElement = document.getElementById("remaining");
const elapsedBar = document.getElementById("elapsedBar");
const remainingBar = document.getElementById("remainingBar");
const phaseElement = document.getElementById("phase");
const nextPhaseElement = document.getElementById("nextPhase");
const selectedPhase = document.getElementById("selectedPhase");
const decisionPhase = document.getElementById("decisionPhase");
const activeIDElement = document.getElementById("activeIDs");
const clockElement = document.getElementById("clock");
const videoTimeElement = document.getElementById("videoTime");

// =========================================
// STATE MANAGEMENT
// =========================================
let remaining = 30;
let elapsed = 0;
let cycleLength = 60;
let currentPhase = "North-South";
let nextPhase = "East-West";
let activeIDs = 24;

// =========================================
// CHART SETUP
// =========================================
const ctx = document.getElementById("trafficChart");
let trafficChart = null;

if (ctx) {
    trafficChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: ["15m", "", "", "12m", "", "", "10m", "", "", "7m", "", "", "5m", "", "", "2m", "", "Now"],
            datasets: [{
                label: "Throughput",
                data: [700, 650, 800, 980, 1100, 1240, 1470, 1510, 1430, 1350, 1210, 1330, 1380, 1320, 1460, 1570, 1740, 1900],
                borderColor: "#3d7dff",
                backgroundColor: "rgba(61,125,255,.08)",
                borderWidth: 2,
                tension: 0.4,
                pointRadius: 0,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    grid: { color: "rgba(255,255,255,.05)" },
                    ticks: { color: "#718492", font: { size: 8 } }
                },
                y: {
                    min: 0,
                    max: 2000,
                    ticks: { color: "#718492", font: { size: 8 }, stepSize: 500 },
                    grid: { color: "rgba(255,255,255,.05)" }
                }
            }
        }
    });
}

// =========================================
// DASHBOARD RENDER
// =========================================
function renderDashboard() {
    if (timer) timer.innerText = remaining;
    if (elapsedElement) elapsedElement.innerText = `${elapsed} s`;
    if (remainingElement) remainingElement.innerText = `${remaining} s`;

    if (phaseElement) phaseElement.innerText = currentPhase;
    if (nextPhaseElement) nextPhaseElement.innerText = nextPhase;
    if (selectedPhase) selectedPhase.innerText = currentPhase;
    if (decisionPhase) decisionPhase.innerText = currentPhase;

    if (activeIDElement) activeIDElement.innerText = activeIDs;

    if (elapsedBar && remainingBar) {
        const elapsedPct = Math.min(100, Math.max(0, (elapsed / cycleLength) * 100));
        const remainingPct = Math.min(100, Math.max(0, (remaining / cycleLength) * 100));
        elapsedBar.style.width = `${elapsedPct}%`;
        remainingBar.style.width = `${remainingPct}%`;
    }
}

// =========================================
// LOCAL 1-SECOND TICKER
// =========================================
// =========================================
// LOCAL 1-SECOND TICKER (NOW ADAPTIVE)
// =========================================
setInterval(() => {
    if (remaining > 0) {
        remaining--;
        elapsed++;
    } else {
        // Phase cycle rollover
        const temp = currentPhase;
        currentPhase = nextPhase;
        nextPhase = temp;
        
        // 2 seconds per vehicle. Min: 15s, Max: 90s.
        let dynamicTime = Math.floor(activeIDs * 2);
        
        if (dynamicTime < 15) {
            dynamicTime = 15;
        } else if (dynamicTime > 90) {
            dynamicTime = 90;
        }
        
        // Apply the AI-calculated time to the next cycle
        remaining = dynamicTime;
        cycleLength = dynamicTime; // Updates the progress bar length
        elapsed = 0;
    }
    renderDashboard();
}, 1000);

// =========================================
// LIVE BACKEND DATA INGESTION
// =========================================
function handleLiveTrafficData(data) {
    if (data.remaining_time !== undefined) remaining = data.remaining_time;
    if (data.elapsed_time !== undefined) elapsed = data.elapsed_time;
    if (data.cycle_length !== undefined) cycleLength = data.cycle_length;
    if (data.current_phase) currentPhase = data.current_phase;
    if (data.next_phase) nextPhase = data.next_phase;
    if (data.total_vehicles !== undefined) activeIDs = data.total_vehicles;
    else if (data.active_ids !== undefined) activeIDs = data.active_ids;

    if (trafficChart && data.throughput) {
        const chartData = trafficChart.data.datasets[0].data;
        chartData.shift();
        chartData.push(data.throughput);
        trafficChart.update("none");
    }

    renderDashboard();
}

// =========================================
// WEBSOCKET & HTTP FALLBACK
// =========================================
const BACKEND_WS_URL = "ws://127.0.0.1:8000/ws";

function connectWebSocket() {
    const ws = new WebSocket(BACKEND_WS_URL);

    ws.onopen = () => {
        console.log("Connected to AI Traffic Backend");
        const statusElem = document.querySelector(".status, [class*='status']");
        if (statusElem) statusElem.innerText = "• System Online (AI Active)";
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleLiveTrafficData(data);
        } catch (err) {
            console.error("Payload error:", err);
        }
    };

    ws.onclose = () => {
        setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = () => {
        // Fallback: poll backend HTTP endpoint if WebSocket is not open
        fetch("http://127.0.0.1:8000/signals/state")
            .then(res => res.json())
            .then(data => handleLiveTrafficData(data))
            .catch(() => {});
    };
}

// =========================================
// CLOCK
// =========================================
function updateClock() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");

    const dateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    if (clockElement) clockElement.innerText = dateTime;
    if (videoTimeElement) videoTimeElement.innerText = dateTime;
}

setInterval(updateClock, 1000);
updateClock();
renderDashboard();
connectWebSocket();