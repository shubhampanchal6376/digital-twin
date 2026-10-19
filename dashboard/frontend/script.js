"use strict";

const API_BASE = "http://127.0.0.1:5000";

const elements = {
    participantId: document.getElementById("participantId"),
    participantMetric: document.getElementById("participantMetric"),
    currentGlucose: document.getElementById("currentGlucose"),
    predictedGlucose: document.getElementById("predictedGlucose"),
    predictionStatus: document.getElementById("predictionStatus"),
    predictionTimestamp: document.getElementById("predictionTimestamp"),
    latestTimestamp: document.getElementById("latestTimestamp"),
    forecastHorizon: document.getElementById("forecastHorizon"),
    connectionStatus: document.getElementById("connectionStatus"),
    messageBox: document.getElementById("messageBox"),
    loadButton: document.getElementById("loadButton"),
    refreshButton: document.getElementById("refreshButton")
};

let forecastChart = null;
let historyChart = null;
let currentParticipantId = null;


function showMessage(message, type = "") {
    elements.messageBox.textContent = message;
    elements.messageBox.className = "message";

    if (type) {
        elements.messageBox.classList.add(type);
    }
}


function formatGlucose(value) {
    const number = Number(value);
    return Number.isFinite(number) ? number.toFixed(1) : "—";
}


function formatTimestamp(value) {
    if (!value) return "—";

    const date = new Date(value);

    return Number.isNaN(date.getTime())
        ? String(value)
        : date.toLocaleString();
}


function setConnectionStatus(connected) {
    elements.connectionStatus.textContent = connected
        ? "API reachable"
        : "API unavailable";
}


function clearCharts() {
    if (forecastChart) {
        forecastChart.destroy();
        forecastChart = null;
    }

    if (historyChart) {
        historyChart.destroy();
        historyChart = null;
    }
}


function clearResults() {
    elements.participantMetric.textContent = "—";
    elements.currentGlucose.textContent = "—";
    elements.predictedGlucose.textContent = "—";
    elements.predictionStatus.textContent = "Waiting";
    elements.predictionTimestamp.textContent = "No prediction loaded";
    elements.latestTimestamp.textContent = "—";

    clearCharts();
}


async function loadParticipants() {
    elements.participantId.replaceChildren();

    const loadingOption = document.createElement("option");
    loadingOption.value = "";
    loadingOption.textContent = "Loading participants...";
    elements.participantId.appendChild(loadingOption);

    try {
        const response = await fetch(`${API_BASE}/api/participants`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not load participants.");
        }

        if (!Array.isArray(data.participants) || data.participants.length === 0) {
            throw new Error("The API returned no participants.");
        }

        elements.participantId.replaceChildren();

        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "Select a participant";
        elements.participantId.appendChild(defaultOption);

        data.participants.forEach((participant) => {
            const option = document.createElement("option");
            option.value = participant;
            option.textContent = participant;
            elements.participantId.appendChild(option);
        });

        showMessage(
            `${data.participants.length} participants available. Select one to begin.`
        );

    } catch (error) {
        console.error("Participant loading failed:", error);

        elements.participantId.replaceChildren();

        const errorOption = document.createElement("option");
        errorOption.value = "";
        errorOption.textContent = "Unable to load participants";
        elements.participantId.appendChild(errorOption);

        showMessage(
            `${error.message} Check that the Flask backend is running.`,
            "error"
        );
    }
}


function renderHistoryChart(readings) {
    const monitorPanel = document.getElementById("monitor");

    let section = document.getElementById("historyChartSection");

    if (!section) {
        section = document.createElement("div");
        section.id = "historyChartSection";

        const heading = document.createElement("h3");
        heading.textContent = "Historical Glucose — Actual Dataset";
        heading.style.margin = "24px 0 12px";

        const container = document.createElement("div");
        container.className = "chart-container";

        const canvas = document.createElement("canvas");
        canvas.id = "historyChart";

        container.appendChild(canvas);
        section.append(heading, container);
        monitorPanel.appendChild(section);
    }

    const canvas = document.getElementById("historyChart");

    if (historyChart) {
        historyChart.destroy();
        historyChart = null;
    }

    historyChart = new Chart(canvas, {
        type: "line",
        data: {
            labels: readings.map(item => formatTimestamp(item.timestamp)),
            datasets: [{
                label: "Observed glucose",
                data: readings.map(item => item.glucose),
                borderColor: "#42d6a4",
                backgroundColor: "rgba(66, 214, 164, 0.10)",
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 4,
                tension: 0.15,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: "index"
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#edf4ff"
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#91a3bb",
                        maxTicksLimit: 8
                    },
                    grid: {
                        color: "rgba(145, 163, 187, 0.1)"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Glucose value",
                        color: "#91a3bb"
                    },
                    ticks: {
                        color: "#91a3bb"
                    },
                    grid: {
                        color: "rgba(145, 163, 187, 0.1)"
                    }
                }
            }
        }
    });
}


function renderForecastChart(result) {
    const canvas = document.getElementById("forecastChart");

    if (!canvas || typeof Chart === "undefined") {
        throw new Error("Chart.js could not be loaded.");
    }

    const current = Number(result.current_glucose);
    const predicted = Number(result.predicted_glucose_2h);

    if (!Number.isFinite(current) || !Number.isFinite(predicted)) {
        throw new Error("The prediction API returned invalid glucose values.");
    }

    const latestDate = new Date(result.latest_timestamp);

    if (Number.isNaN(latestDate.getTime())) {
        throw new Error("The prediction API returned an invalid timestamp.");
    }

    const horizon = Number(result.prediction_horizon_minutes || 120);

    const forecastDate = new Date(
        latestDate.getTime() + horizon * 60 * 1000
    );

    if (forecastChart) {
        forecastChart.destroy();
    }

    forecastChart = new Chart(canvas, {
        type: "line",
        data: {
            labels: [
                formatTimestamp(result.latest_timestamp),
                formatTimestamp(forecastDate.toISOString())
            ],
            datasets: [{
                label: "Observed / predicted glucose",
                data: [current, predicted],
                borderColor: "#42d9e8",
                backgroundColor: "rgba(66, 217, 232, 0.12)",
                borderWidth: 3,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: ["#42d6a4", "#658cff"],
                tension: 0,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: "index"
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#edf4ff"
                    }
                },
                tooltip: {
                    callbacks: {
                        label: context =>
                            `${context.parsed.y.toFixed(1)} glucose units`
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#91a3bb",
                        maxRotation: 30,
                        minRotation: 0
                    },
                    grid: {
                        color: "rgba(145, 163, 187, 0.1)"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Glucose value",
                        color: "#91a3bb"
                    },
                    ticks: {
                        color: "#91a3bb"
                    },
                    grid: {
                        color: "rgba(145, 163, 187, 0.1)"
                    }
                }
            }
        }
    });
}


async function loadParticipant() {
    const participantId = elements.participantId.value;

    if (!participantId) {
        showMessage("Select a participant first.", "error");
        return;
    }

    currentParticipantId = participantId;
    elements.loadButton.disabled = true;
    elements.refreshButton.disabled = true;

    clearResults();
    elements.predictionStatus.textContent = "Loading";

    showMessage(
        "Loading historical readings and generating the experimental forecast...",
        "loading"
    );

    try {
        const [historyResponse, predictionResponse] = await Promise.all([
            fetch(`${API_BASE}/api/cgm/${encodeURIComponent(participantId)}`),
            fetch(`${API_BASE}/api/predict/${encodeURIComponent(participantId)}`)
        ]);

        const [history, prediction] = await Promise.all([
            historyResponse.json(),
            predictionResponse.json()
        ]);

        if (!historyResponse.ok) {
            throw new Error(history.error || "Could not load CGM history.");
        }

        if (!predictionResponse.ok) {
            throw new Error(prediction.error || "Could not generate prediction.");
        }

        if (
            history.participant_id !== participantId ||
            prediction.participant_id !== participantId
        ) {
            throw new Error("The returned participant ID does not match.");
        }

        if (!Array.isArray(history.readings) || history.readings.length === 0) {
            throw new Error("No historical readings were returned.");
        }

        const readings = history.readings
            .map(item => ({
                timestamp: item.timestamp,
                date: new Date(item.timestamp),
                glucose: Number(item.glucose)
            }))
            .filter(item =>
                !Number.isNaN(item.date.getTime()) &&
                Number.isFinite(item.glucose)
            );

        if (readings.length === 0) {
            throw new Error("No valid historical readings were returned.");
        }

        elements.participantMetric.textContent = participantId;
        elements.currentGlucose.textContent =
            formatGlucose(prediction.current_glucose);
        elements.predictedGlucose.textContent =
            formatGlucose(prediction.predicted_glucose_2h);

        elements.predictionStatus.textContent = "Received";

        const horizon = Number(prediction.prediction_horizon_minutes || 120);

        elements.predictionTimestamp.textContent = `${horizon} minutes ahead`;
        elements.forecastHorizon.textContent = `${horizon} minutes`;
        elements.latestTimestamp.textContent =
            formatTimestamp(prediction.latest_timestamp);

        renderHistoryChart(readings);
        renderForecastChart(prediction);

        setConnectionStatus(true);

        showMessage(
            `Loaded ${readings.length} historical readings and the experimental forecast. Not medical advice.`,
            "success"
        );

    } catch (error) {
        console.error("Participant loading failed:", error);

        clearResults();
        elements.predictionStatus.textContent = "Unavailable";

        showMessage(error.message, "error");

    } finally {
        elements.loadButton.disabled = false;
        elements.refreshButton.disabled = false;
    }
}


async function checkApiConnection() {
    try {
        const response = await fetch(`${API_BASE}/`);

        if (!response.ok) {
            setConnectionStatus(false);
            return;
        }

        const result = await response.json();
        setConnectionStatus(result.status === "running");

    } catch (error) {
        console.warn("Flask API is unavailable:", error.message);
        setConnectionStatus(false);
    }
}


elements.loadButton.addEventListener("click", loadParticipant);

elements.refreshButton.addEventListener("click", async () => {
    await checkApiConnection();

    if (currentParticipantId) {
        elements.participantId.value = currentParticipantId;
        await loadParticipant();
    } else {
        await loadParticipants();
        showMessage("Select a participant to load the readings and forecast.");
    }
});

elements.participantId.addEventListener("change", () => {
    if (elements.participantId.value) {
        showMessage(
            `Selected ${elements.participantId.value}. Click Load Participant.`
        );
    }
});

document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
        document.querySelectorAll(".nav-link").forEach(item => {
            item.classList.remove("active");
        });

        link.classList.add("active");
    });
});


checkApiConnection();
loadParticipants();