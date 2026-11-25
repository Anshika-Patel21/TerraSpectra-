
import './App.css'
import { useEffect, useMemo, useState } from 'react'
import FarmSummary from './components/FarmSummary'
import ChemicalAnomalies from './components/ChemicalAnomalies'

import HeatmapMap from './components/HeatmapMap'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import MetricCard from './components/MetricCard'
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
  const [riskFilter, setRiskFilter] = useState(() => {
  return localStorage.getItem('terraSpectraRiskFilter') || 'All'
})
useEffect(() => {
  localStorage.setItem('terraSpectraRiskFilter', riskFilter)
}, [riskFilter])
  const [selectedZone, setSelectedZone] = useState(null)
  const [activeTab, setActiveTab] = useState('Overview')
  const [showDataLabels, setShowDataLabels] = useState(() => {
  return localStorage.getItem('terraSpectraShowDataLabels') !== 'false'
})

  const [theme, setTheme] = useState(() => {
  return localStorage.getItem('terraSpectraTheme') || 'dark'
})

useEffect(() => {
  localStorage.setItem(
    'terraSpectraShowDataLabels',
    String(showDataLabels)
  )
}, [showDataLabels])
useEffect(() => {
  localStorage.setItem('terraSpectraTheme', theme)
}, [theme])
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
    <div className={`dashboard ${theme}`}>
      <Sidebar
         activeTab={activeTab}
         onNavigate={setActiveTab}
      />

      <div className="main-area">
        <Header />

        <main className="content">
          {activeTab === 'Overview' && (
  <>
          <div className="page-heading">
            <div>
              <h1>Welcome to TerraSpectra</h1>
              <p>Hyperspectral Crop Monitoring & Risk Analysis</p>
            </div>

             {showDataLabels && (
  <span className="demo-label">SAMPLE MAP</span>
)}
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
<FarmSummary />
          <section className="map-section">
            <div className="section-heading">
              <div>
                <h2>Geospatial Risk Overview</h2>
                <p>Pixel-level crop risk visualization</p>
              </div>

              {showDataLabels && (
                <span className="demo-label">SAMPLE MAP</span>
        )}
            </div>

            <div className="risk-filter-controls">
              <span>Filter risk:</span>

              {['All', 'Low', 'Medium', 'High'].map((risk) => (
                <button
                  key={risk}
                  className={riskFilter === risk ? 'active' : ''}
                  onClick={() => setRiskFilter(risk)}
                >
                  {risk}
                </button>
              ))}
            </div>

            <HeatmapMap
              riskFilter={riskFilter}
              onZoneSelect={setSelectedZone}
            />
          </section>

          <RiskAnalytics />

          <RiskChart />
          <ChemicalAnomalies />
          <PredictionOverview zones={filteredZones} />

          <ForecastChart zones={filteredZones} />

          <ZonePrediction selectedZone={selectedZone} />
          </>
)}

{activeTab === 'GIS Map' && (
  <>
    <div className="page-heading">
      <div>
        <h1>Geospatial Risk Map</h1>
        <p>Explore crop risk across monitored farm zones</p>
      </div>
      {showDataLabels && (
  <span className="demo-label">SAMPLE MAP</span>
)}
    </div>

    <div className="risk-filter-controls">
      <span>Filter risk:</span>
      {['All', 'Low', 'Medium', 'High'].map((risk) => (
        <button
          key={risk}
          className={riskFilter === risk ? 'active' : ''}
          onClick={() => setRiskFilter(risk)}
        >
          {risk}
        </button>
      ))}
    </div>

    <HeatmapMap
      riskFilter={riskFilter}
      onZoneSelect={setSelectedZone}
    />

    <ZonePrediction selectedZone={selectedZone} />
  </>
)}

{activeTab === 'Analytics' && (
  <>
    <div className="page-heading">
      <div>
        <h1>Farm Analytics</h1>
        <p>Risk distribution and spectral anomaly indicators</p>
      </div>
      {showDataLabels && (
  <span className="demo-label">SAMPLE MAP</span>
)}
    </div>

    <FarmSummary />
    <RiskAnalytics />
    <RiskChart />
    <ChemicalAnomalies />
    <PredictionOverview zones={filteredZones} />
    <ForecastChart zones={filteredZones} />
  </>
)}

{activeTab === 'Historical Data' && (
  <div className="page-heading">
    <div>
      <h1>Historical Data</h1>
      <p>Review historical crop health and disease trends</p>
      <p>
        Historical records are not yet connected.
        This section will become available when dated
        observations and prediction data are integrated.
      </p>
      <span className="demo-label">AWAITING DATA INTEGRATION</span>
    </div>
  </div>
)}


{activeTab === 'Settings' && (
  <>
    <div className="page-heading">
      <div>
        <h1>Settings</h1>
        <p>Manage your dashboard preferences and configuration</p>
      </div>
      <span className="demo-label">CONFIGURATION</span>
    </div>

    <div className="settings-grid">

      <section className="settings-card">
        <h2>Map Preferences</h2>
        <p className="settings-description">
          Configure your GIS map behaviour
        </p>

        <div className="settings-row">
          <div>
            <h3>Default Risk Filter</h3>
            <p>Choose your preferred risk category</p>
          </div>

          <select
            value={riskFilter}
            onChange={(e) => {
              setRiskFilter(e.target.value)
              setSelectedZone(null)
            }}
          >
            <option value="All">All Risks</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </div>

        <div className="settings-row">
          <div>
            <h3>Reset Map</h3>
            <p>Clear selected zones and risk filters</p>
          </div>

          <button
            className="settings-button"
            onClick={() => {
              setRiskFilter('All')
              setSelectedZone(null)
            }}
          >
            Reset Filters
          </button>
        </div>
      </section>

      <section className="settings-card">
        <h2>Display Preferences</h2>
        <p className="settings-description">
          Current dashboard display configuration
        </p>

        <div className="settings-row">
          <div>
            <h3>Dashboard Theme</h3>
            <p>Current application appearance</p>
            <select
  value={theme}
  onChange={(e) => setTheme(e.target.value)}
>
  <option value="dark">Dark Mode</option>
  <option value="light">Light Mode</option>
</select>
          </div>
          <span className="settings-status">
  {theme === 'dark' ? 'Dark Mode' : 'Light Mode'}
</span>
        </div>

       <div className="settings-row">
         <div>
           <h3>Data Labels</h3>
             <p>Show or hide synthetic data indicators</p>
         </div>

         <label className="settings-toggle">
           <input
             type="checkbox"
             checked={showDataLabels}
             onChange={(e) => setShowDataLabels(e.target.checked)}
           />
           <span>{showDataLabels ? 'Visible' : 'Hidden'}</span>
         </label>
       </div>
      </section>

      <section className="settings-card">
        <h2>About TerraSpectra</h2>
        <p className="settings-description">
          Application information
        </p>

        <div className="settings-row">
          <h3>Application</h3>
          <span>TerraSpectra</span>
        </div>

        <div className="settings-row">
          <h3>Version</h3>
          <span>Development</span>
        </div>

        <div className="settings-row">
          <h3>Data Mode</h3>
          {showDataLabels && (
  <span className="demo-label">SAMPLE MAP</span>
)}
        </div>
      </section>

    </div>
  </>
)}

</main>
</div>
</div>
)
}

export default App