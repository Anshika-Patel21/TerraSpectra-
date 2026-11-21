
import { useEffect, useMemo, useState } from 'react'

import './App.css'

import GISMap from './components/GISMap'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import MetricCard from './components/MetricCard'
import RiskLegend from './components/RiskLegend'
import RiskAnalytics from './components/RiskAnalytics'
import RiskChart from './components/RiskChart'
import PredictionOverview from './components/PredictionOverview'
import ForecastChart from './components/ForecastChart'
import ZonePrediction from './components/ZonePrediction'

import {
  farmSummary,
  getHighRiskPercentage,
} from './data/riskData'

import { farmZones } from './data/farmZones'

function App() {
  const [riskFilter, setRiskFilter] = useState('All')
  const [selectedZone, setSelectedZone] = useState(null)

  const filteredZones = useMemo(() => {
    if (riskFilter === 'All') {
      return farmZones
    }

    return {
      ...farmZones,
      features: farmZones.features.filter(
        (feature) => feature.properties.risk === riskFilter
      ),
    }
  }, [riskFilter])

  useEffect(() => {
    if (
      selectedZone &&
      !filteredZones.features.some(
        (feature) => feature.properties.id === selectedZone.id
      )
    ) {
      setSelectedZone(null)
    }
  }, [filteredZones, selectedZone])

  return (
    <div className="dashboard">
      <Sidebar />

      <div className="main-area">
        <Header />

        <main className="content">
          <div className="page-heading">
            <div>
              <h1>Welcome to TerraSpectra</h1>
              <p>Hyperspectral Crop Monitoring & Risk Analysis</p>
            </div>

            <span className="demo-label">DEMO DATA</span>
          </div>

          <div className="metrics-grid">
            <MetricCard
              title="Total Monitored Area"
              value={farmSummary.totalArea.toLocaleString()}
              unit="acres"
              description="Illustrative farm area"
            />

            <MetricCard
              title="High-Risk Area"
              value={farmSummary.highRiskArea}
              unit="acres"
              description={`${getHighRiskPercentage()}% of monitored area · Synthetic risk estimate`}
              variant="high-risk"
            />

            <MetricCard
              title="Monitored Zones"
              value={farmSummary.monitoredZones}
              unit="zones"
              description="Sample monitoring zones"
            />
          </div>

          <section className="map-section">
            <div className="section-heading">
              <div>
                <h2>Geospatial Risk Overview</h2>
                <p>Farm monitoring and crop stress visualization</p>
              </div>

              <span className="demo-label">SAMPLE MAP</span>
            </div>

            <GISMap
              riskFilter={riskFilter}
              onRiskFilterChange={setRiskFilter}
              zones={filteredZones}
              selectedZone={selectedZone}
              onZoneSelect={setSelectedZone}
            />

            <RiskLegend />
          </section>

          <RiskAnalytics zones={filteredZones} />

          <RiskChart zones={filteredZones} />

          <PredictionOverview zones={filteredZones} />

          <ForecastChart zones={filteredZones} />

          <ZonePrediction selectedZone={selectedZone} />
        </main>
      </div>
    </div>
  )
}

export default App




