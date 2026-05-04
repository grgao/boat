import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./App.css"; 

const MapComponent = () => {
  const boatPosition = [43.0722, -89.4008]; // Static boat position (API will update this later)
  const [destination, setDestination] = useState(null);
  const [mode, setMode] = useState("manual"); // "manual" or "route"

  return (
    <div className="map-container">
      <h1>Boat Navigation</h1>

      {/* Mode Selection */}
      <div className="mode-buttons">
        <button className={mode === "manual" ? "active" : ""} onClick={() => setMode("manual")}>
          🚤 Manual Control
        </button>
        <button className={mode === "route" ? "active" : ""} onClick={() => setMode("route")}>
          📍 Plan a Route
        </button>
      </div>

      {/* Map Display */}
      <MapContainer center={boatPosition} zoom={13} scrollWheelZoom={false} className="leaflet-map">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Boat Marker */}
        <Marker position={boatPosition}>
          <Popup>Boat Position</Popup>
        </Marker>

        {/* Destination Marker (Only shows in route mode) */}
        {mode === "route" && destination && (
          <Marker position={destination}>
            <Popup>Destination</Popup>
          </Marker>
        )}
      </MapContainer>

      {/* Manual Control UI (Only shows if manual mode is selected) */}
      {mode === "manual" && (
        <div className="controls">
          <button>⬆️ Forward</button>
          <button>⬅️ Left</button>
          <button>➡️ Right</button>
          <button>⬇️ Backward</button>
        </div>
      )}

      {/* Route Planning UI (Only shows if route mode is selected) */}
      {mode === "route" && (
        <div className="route-input">
          <input
            type="text"
            placeholder="Enter Lat,Lng (e.g. 43.074,-89.381)"
            onChange={(e) => {
              const [lat, lng] = e.target.value.split(",").map(Number);
              if (!isNaN(lat) && !isNaN(lng)) setDestination([lat, lng]);
            }}
          />
          <button>Set Destination</button>
        </div>
      )}
    </div>
  );
};

export default MapComponent;
