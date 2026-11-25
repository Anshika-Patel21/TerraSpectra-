import './HeatmapMap.css'

import { useEffect, useRef, useState } from 'react'
import {
  Map,
  NavigationControl,
  setWorkerUrl,
} from 'maplibre-gl'

import { MapLibreOverlay } from '@deck.gl/maplibre'

import maplibreWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url'
import { PolygonLayer } from '@deck.gl/layers'

import { heatmapData } from '../data/heatmapData'
import { farmZones } from '../data/farmZones'

import 'maplibre-gl/dist/maplibre-gl.css'
setWorkerUrl(maplibreWorkerUrl)
const riskColors = {
  Low: [74, 222, 128, 170],
  Medium: [250, 204, 21, 180],
  High: [251, 113, 133, 190],
}

function HeatmapMap({ riskFilter, onZoneSelect }) {
  const mapContainer = useRef(null)
  const mapRef = useRef(null)
  const overlayRef = useRef(null)

  const [mapReady, setMapReady] = useState(false)
  const [hoveredPixel, setHoveredPixel] = useState(null)

  useEffect(() => {
    if (!mapContainer.current) return

    const map = new Map({
      container: mapContainer.current,
      style: 'https://tiles.openfreemap.org/styles/liberty',
      center: [79.957, 23.185],
      zoom: 12.5,
      pitch: 0,
      bearing: 0,
      antialias: true,
    })

    mapRef.current = map

    map.addControl(
      new NavigationControl(),
      'top-right'
    )

    map.on('load', () => {
      const overlay = new MapLibreOverlay({
        interleaved: true,
        layers: [],
      })

      overlayRef.current = overlay
      map.addControl(overlay)
      setMapReady(true)
    })

    return () => {
      map.remove()
      mapRef.current = null
      overlayRef.current = null
    }
  }, [])

  useEffect(() => {
    if (!mapReady || !overlayRef.current) return

    const visiblePixels = heatmapData.filter((pixel) => {
      return riskFilter === 'All' || pixel.risk === riskFilter
    })

    const heatmapLayer = new PolygonLayer({
      id: 'farm-heatmap-layer',
      data: visiblePixels,

      getPolygon: (pixel) => pixel.polygon,

      getFillColor: (pixel) => riskColors[pixel.risk],
      getLineColor: [255, 255, 255, 180],

      getLineWidth: 1,
      lineWidthUnits: 'pixels',

      filled: true,
      stroked: true,
      pickable: true,
      autoHighlight: true,
      highlightColor: [255, 255, 255, 100],
    })

    overlayRef.current.setProps({
      layers: [heatmapLayer],

      onHover: (info) => {
        if (info.object) {
          setHoveredPixel({
            ...info.object,
            x: info.x,
            y: info.y,
          })
        } else {
          setHoveredPixel(null)
        }
      },

      onClick: (info) => {
        if (!info.object) return

        const selectedFeature = farmZones.features.find(
          (feature) =>
            feature.properties.id === info.object.zoneId
        )

        if (selectedFeature) {
          onZoneSelect?.(selectedFeature.properties)
        }
      },
    })
  }, [mapReady, riskFilter, onZoneSelect])

  return (
    <div className="heatmap-wrapper">
      <div className="heatmap-heading">
        <div>
          <h3>Farm Risk Heatmap</h3>
          <p>Pixel-level risk distribution across monitored zones</p>
        </div>

        <span className="heatmap-status">DEMO DATA</span>
      </div>

      <div className="heatmap-map-container">
        <div ref={mapContainer} className="heatmap-map" />

        {hoveredPixel && (
          <div
            className="heatmap-tooltip"
            style={{
              left: hoveredPixel.x + 12,
              top: hoveredPixel.y + 12,
            }}
          >
            <strong>{hoveredPixel.id}</strong>
            <span>{hoveredPixel.zoneName}</span>
            <span>Risk: {hoveredPixel.risk}</span>
            <span>Risk Score: {hoveredPixel.riskScore}%</span>
          </div>
        )}
      </div>

      <div className="heatmap-legend">
        <span><i className="legend-low" /> Low Risk</span>
        <span><i className="legend-medium" /> Medium Risk</span>
        <span><i className="legend-high" /> High Risk</span>
      </div>
    </div>
  )
}

export default HeatmapMap
