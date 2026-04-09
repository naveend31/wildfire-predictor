// Main Application Logic
const API_BASE = 'http://localhost:8000/api';

// Initialize map, centered near Sacramento
const map = L.map('map', {
    zoomControl: false // custom position later
}).setView([38.5, -121.0], 9);

L.control.zoom({
    position: 'topright'
}).addTo(map);

// Add dark CartoDB tile layer
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

// Map Layers
let fireMarkersLayer = L.layerGroup().addTo(map);
let spreadPolygonsLayer = L.layerGroup().addTo(map);

const DOM = {
    slider: document.getElementById('time-slider'),
    hoursDisplay: document.getElementById('hours-display'),
    btnOptimize: document.getElementById('btn-optimize'),
    allocationsList: document.getElementById('allocations-list'),
    loading: document.getElementById('loading'),
    inTankers: document.getElementById('input-tankers'),
    inCrews: document.getElementById('input-crews')
};

// Global State
let activeFires = [];

// API Calls
async function fetchFires() {
    try {
        const res = await fetch(`${API_BASE}/fires`);
        activeFires = await res.json();
        renderFireMarkers();
    } catch (e) {
        console.error("Error fetching fires", e);
    }
}

async function fetchSpread(hours) {
    if (hours == 0) {
        spreadPolygonsLayer.clearLayers();
        return;
    }
    
    showLoading(true);
    try {
        const res = await fetch(`${API_BASE}/simulate?hours=${hours}`);
        const geojson = await res.json();
        renderSpread(geojson);
    } catch (e) {
        console.error("Error simulating spread", e);
    } finally {
        showLoading(false);
    }
}

async function runOptimization() {
    showLoading(true);
    const tankers = DOM.inTankers.value;
    const crews = DOM.inCrews.value;
    
    try {
        const res = await fetch(`${API_BASE}/optimize?tankers=${tankers}&crews=${crews}`);
        const data = await res.json();
        renderAllocations(data);
    } catch (e) {
        console.error("Error optimizing", e);
    } finally {
        showLoading(false);
    }
}

// Renderers
function renderFireMarkers() {
    fireMarkersLayer.clearLayers();
    activeFires.forEach(fire => {
        // Red glowing circle for active fire
        const marker = L.circleMarker([fire.lat, fire.lng], {
            radius: 8,
            fillColor: "#ff4500",
            color: "#fff",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        });
        
        marker.bindPopup(`
            <strong>${fire.name}</strong><br/>
            Severity: ${fire.severity}/10<br/>
            Wind: ${fire.wind_speed.toFixed(1)} km/h @ ${fire.wind_dir.toFixed(0)}&deg;
        `);
        
        fireMarkersLayer.addLayer(marker);
    });
}

function renderSpread(geojson) {
    spreadPolygonsLayer.clearLayers();
    
    L.geoJSON(geojson, {
        style: function(feature) {
            return {
                fillColor: "#ff4500",
                fillOpacity: 0.3,
                color: "#ff5722",
                weight: 2,
                dashArray: "4 4"
            };
        },
        onEachFeature: function(feature, layer) {
            layer.bindPopup(`Projected +${feature.properties.hours_ahead}h spread area`);
        }
    }).addTo(spreadPolygonsLayer);
}

function renderAllocations(data) {
    DOM.allocationsList.innerHTML = '';
    
    if (!data.allocations || data.allocations.length === 0) {
        DOM.allocationsList.innerHTML = '<p class="muted">No resources allocated.</p>';
        return;
    }
    
    // Sort by threat to show worst first
    data.allocations.sort((a, b) => b.threat_score - a.threat_score);
    
    data.allocations.forEach(alloc => {
        const fire = activeFires.find(f => f.id === alloc.fire_id);
        const name = fire ? fire.name : alloc.fire_id;
        
        const card = document.createElement('div');
        card.className = 'allocation-card';
        card.innerHTML = `
            <h4>${name} (Threat: ${alloc.threat_score.toFixed(1)})</h4>
            <p>Air Tankers: <span>${alloc.air_tankers}</span> | Ground Crews: <span>${alloc.ground_crews}</span></p>
        `;
        DOM.allocationsList.appendChild(card);
        
        // Draw connection lines on map from a theoretical base
        // Or just zoom to the most threatened fire
    });
    
    // Summary
    const summary = document.createElement('div');
    summary.style.marginTop = "15px";
    summary.innerHTML = `<p class="muted">Remaining Reserve: ${data.remaining_tankers} Tankers, ${data.remaining_crews} Crews.</p>`;
    DOM.allocationsList.appendChild(summary);
}

// Utils
function showLoading(show) {
    if (show) DOM.loading.classList.remove('hidden');
    else DOM.loading.classList.add('hidden');
}

// Events
DOM.slider.addEventListener('input', (e) => {
    DOM.hoursDisplay.innerText = e.target.value + 'h';
});
DOM.slider.addEventListener('change', (e) => {
    fetchSpread(parseInt(e.target.value));
});

DOM.btnOptimize.addEventListener('click', () => {
    runOptimization();
});

// Init
fetchFires();
