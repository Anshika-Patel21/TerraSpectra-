

import { useEffect } from 'react'

import {
  MapContainer,
  TileLayer,
  GeoJSON,
  useMap,
} from 'react-leaflet'

import L from 'leaflet'
import { farmZones } from '../data/farmZones'

const riskColors = {
  Low: '#4ade80',
  Medium: '#facc15',
  High: '#fb7185',
}

const filters = ['All', 'Low', 'Medium', 'High']

function MapBounds({ zones }) {
  const map = useMap()

  useEffect(() => {
    if (!zones.features.length) return

    const bounds = L.geoJSON(zones).getBounds()

    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [40, 40] })
    }
  }, [map, zones])

  return null
}

function GISMap({
  riskFilter,
  onRiskFilterChange,
  zones,
  selectedZone,
  onZoneSelect,
}) {
  const getZoneStyle = (feature) => {
    const risk = feature.properties.risk
    const isSelected = selectedZone?.id === feature.properties.id

    return {
      fillColor: riskColors[risk],
      color: riskColors[risk],
      weight: isSelected ? 4 : 2,
      fillOpacity: isSelected ? 0.75 : 0.45,
    }
  }

  const handleEachZone = (feature, layer) => {
    const { name, risk, area, id } = feature.properties

    layer.bindPopup(`
      <strong>${name}</strong><br/>
      Risk Level: ${risk}<br/>
      Area: ${area} acres
    `)

    layer.on({
      click: () => {
        onZoneSelect({ id, name, risk, area })
      },

      mouseover: (event) => {
        event.target.setStyle({
          weight: 4,
          fillOpacity: 0.75,
        })
      },

      mouseout: (event) => {
        event.target.setStyle(getZoneStyle(feature))
      },
    })
  }

  return (
    <div className="gis-map-container">

      <div className="risk-filter">
        <span className="risk-filter-label">FILTER BY RISK</span>

        <div className="risk-filter-options">
          {filters.map((filter) => (
            <button
              key={filter}
              type="button"
              className={`risk-filter-button ${
                riskFilter === filter ? 'active' : ''
              }`}
              onClick={() => onRiskFilterChange(filter)}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      <div className="gis-map">
        <MapContainer
          center={[23.185, 79.957]}
          zoom={15}
          scrollWheelZoom={true}
          className="leaflet-map"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <GeoJSON
            key={`${riskFilter}-${selectedZone?.id ?? 'none'}`}
            data={zones}
            style={getZoneStyle}
            onEachFeature={handleEachZone}
          />

          <MapBounds zones={zones} />
        </MapContainer>
      </div>

      <section className="selected-zone-panel">
        <div className="selected-zone-heading">
          <h3>Selected Farm Zone</h3>
          <span>ZONE DETAILS</span>
        </div>

        {selectedZone ? (
          <div className="selected-zone-details">
            <div>
              <p>Zone Name</p>
              <h4>{selectedZone.name}</h4>
            </div>

            <div>
              <p>Risk Classification</p>
              <span className={`risk-badge risk-${selectedZone.risk.toLowerCase()}`}>
                {selectedZone.risk} Risk
              </span>
            </div>

            <div>
              <p>Monitored Area</p>
              <h4>{selectedZone.area} acres</h4>
            </div>
          </div>
        ) : (
          <p className="no-zone-selected">
            Select a coloured zone on the map to view its details.
          </p>
        )}
      </section>
    </div>
  )
}

export default GISMap
