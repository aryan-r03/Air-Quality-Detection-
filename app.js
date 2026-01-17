// Air Quality Prediction App - Frontend Logic

// DOM Elements
const form = document.getElementById('airQualityForm');
const loading = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const analyzeBtn = document.getElementById('analyzeBtn');

// Preset configurations for quick testing
const PRESETS = {
    good: {
        temperature: 22,
        humidity: 55,
        pm25: 15,
        pm10: 25,
        no2: 20,
        so2: 10,
        co: 0.3,
        o3: 40
    },
    moderate: {
        temperature: 28,
        humidity: 65,
        pm25: 45,
        pm10: 65,
        no2: 50,
        so2: 30,
        co: 1.2,
        o3: 80
    },
    unhealthy: {
        temperature: 32,
        humidity: 70,
        pm25: 120,
        pm10: 180,
        no2: 100,
        so2: 70,
        co: 3.5,
        o3: 140
    }
};

/**
 * Load preset air quality values
 */
function loadGoodAir() {
    loadPreset(PRESETS.good);
}

function loadModerateAir() {
    loadPreset(PRESETS.moderate);
}

function loadUnhealthyAir() {
    loadPreset(PRESETS.unhealthy);
}

function loadPreset(preset) {
    Object.keys(preset).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            element.value = preset[key];
        }
    });
}

/**
 * Clear the form
 */
function clearForm() {
    form.reset();
    resultDiv.style.display = 'none';
}

/**
 * Collect form data
 */
function collectFormData() {
    return {
        temperature: parseFloat(document.getElementById('temperature').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        pm25: parseFloat(document.getElementById('pm25').value),
        pm10: parseFloat(document.getElementById('pm10').value),
        no2: parseFloat(document.getElementById('no2').value),
        so2: parseFloat(document.getElementById('so2').value),
        co: parseFloat(document.getElementById('co').value),
        o3: parseFloat(document.getElementById('o3').value)
    };
}

/**
 * Make prediction API call
 */
async function makePrediction(features) {
    const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ features: features })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

/**
 * Display prediction result
 */
function displayResult(result) {
    const colorClass = result.color;

    resultDiv.innerHTML = `
        <div class="result-container">
            <div class="aqi-circle ${colorClass}">
                <div class="aqi-value">${Math.round(result.aqi)}</div>
                <div class="aqi-label">AQI</div>
            </div>

            <div class="category-title ${colorClass}">${result.category}</div>
            <div class="health-text">${result.health_implication}</div>

            <div class="info-box">
                <div class="info-box-title">ℹ️ About Air Quality Index</div>
                <div class="info-box-text">
                    The Air Quality Index (AQI) is calculated based on multiple pollutants including PM2.5, PM10, NO2, SO2, CO, and O3. This prediction is generated using machine learning algorithms trained on environmental data. For official air quality information, please consult your local environmental protection agency.
                </div>
            </div>
        </div>
    `;

    resultDiv.style.display = 'flex';
}

/**
 * Display error message
 */
function displayError(errorMessage) {
    resultDiv.innerHTML = `
        <div class="result-container">
            <div class="aqi-circle" style="border-color: #666; background: rgba(100, 100, 100, 0.2);">
                <div class="aqi-value">--</div>
                <div class="aqi-label">ERROR</div>
            </div>

            <div class="category-title" style="color: #999;">CALCULATION ERROR</div>
            <div class="health-text">Unable to calculate AQI. Please check your inputs.</div>

            <div class="info-box">
                <div class="info-box-title">⚠️ Error Details</div>
                <div class="info-box-text">${errorMessage}</div>
            </div>
        </div>
    `;

    resultDiv.style.display = 'flex';
}

/**
 * Handle form submission
 */
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Collect form data
    const features = collectFormData();

    // Update UI to show loading state
    analyzeBtn.disabled = true;
    loading.style.display = 'flex';
    resultDiv.style.display = 'none';

    try {
        // Make API call
        const data = await makePrediction(features);

        // Display result or error
        if (data.success) {
            displayResult(data.result);
        } else {
            displayError(data.error || 'Unknown error occurred');
        }
    } catch (error) {
        displayError(error.message);
    } finally {
        // Reset UI state
        analyzeBtn.disabled = false;
        loading.style.display = 'none';
    }
});

/**
 * Initialize app with good air preset
 */
window.addEventListener('load', () => {
    loadGoodAir();
});
