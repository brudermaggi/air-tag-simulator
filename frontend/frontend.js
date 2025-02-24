let map;
let markers = {};
let currentEditingId = null;

// Karte initialisieren
function initMap() {
    map = L.map('map').setView([51.1657, 10.4515], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
}

// Airtag Liste aktualisieren
async function updateAirtagList() {
    const response = await fetch('http://localhost:8000/tags');
    const airtags = await response.json();
    
    const listContainer = document.getElementById('airtagList');
    listContainer.innerHTML = '';

    airtags.forEach(tag => {
        const element = document.createElement('div');
        element.className = 'bg-gray-50 p-3 rounded-lg shadow-sm';
        element.innerHTML = `
            <div class="flex justify-between items-center">
                <div>
                    <h3 class="font-semibold">${tag.name || `Airtag ${tag.id}`}</h3>
                    <p class="text-sm text-gray-500">ID: ${tag.id}</p>
                </div>
                <div class="space-x-2">
                    <button onclick="showNameModal(${tag.id})" class="text-blue-500 hover:text-blue-700">✏️</button>
                    <button onclick="deleteAirtag(${tag.id})" class="text-red-500 hover:text-red-700">🗑️</button>
                </div>
            </div>
        `;
        listContainer.appendChild(element);
    });

    updateMapMarkers(airtags);
}

// Karten-Marker aktualisieren
function updateMapMarkers(airtags) {
    // Alte Marker entfernen
    Object.values(markers).forEach(marker => marker.remove());
    markers = {};

    // Neue Marker hinzufügen
    airtags.forEach(tag => {
        if (tag.lat && tag.lon) {
            const marker = L.marker([tag.lat, tag.lon])
                .addTo(map)
                .bindPopup(`<b>${tag.name || `Airtag ${tag.id}`}</b><br>ID: ${tag.id}`);
            markers[tag.id] = marker;
        }
    });
}

// Airtag hinzufügen
async function addAirtag() {
    const tagId = document.getElementById('tagId').value;
    if (!tagId) return;

    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: parseInt(tagId)})
        });

        if (response.ok) {
            updateAirtagList();
            document.getElementById('tagId').value = '';
        }
    } catch (error) {
        console.error('Fehler beim Hinzufügen:', error);
    }
}

// Airtag löschen
async function deleteAirtag(id) {
    try {
        const response = await fetch(`http://localhost:8000/tags/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            updateAirtagList();
        }
    } catch (error) {
        console.error('Fehler beim Löschen:', error);
    }
}

// Sound abspielen
async function playSound(id) {
    try {
        await fetch(`http://localhost:8000/tone`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id})
        });
    } catch (error) {
        console.error('Fehler beim Ton abspielen:', error);
    }
}

// Namensänderungs-Modal
function showNameModal(id) {
    currentEditingId = id;
    document.getElementById('nameModal').classList.remove('hidden');
}

function closeNameModal() {
    document.getElementById('nameModal').classList.add('hidden');
    currentEditingId = null;
}

async function saveTagName() {
    const name = document.getElementById('tagName').value;
    if (!name || !currentEditingId) return;

    try {
        const response = await fetch(`http://localhost:8000/tags/${currentEditingId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name})
        });

        if (response.ok) {
            updateAirtagList();
            closeNameModal();
        }
    } catch (error) {
        console.error('Fehler beim Speichern:', error);
    }
}

// Initialisierung
initMap();
updateAirtagList();
setInterval(updateAirtagList, 15000); // Automatische Aktualisierung alle 15 Sekunden