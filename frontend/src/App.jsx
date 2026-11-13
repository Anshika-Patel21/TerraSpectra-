import {
  riskData,
  farmSummary,
  getHighRiskPercentage,
} from './data/riskData'
import './App.css'

function App() {


  return (
    <div className="dashboard">

      {/* Sidebar */}
      <aside className="sidebar">
        <h2>TerraSpectra</h2>
        <nav>
          <p>Overview</p>
          <p>GIS Map</p>
          <p>Analytics</p>
          <p>Historical Data</p>
          <p>Settings</p>
        </nav>
      </aside>

      {/* Main workspace */}
      <div className="main-area">

        {/* Header */}
        <header className="header">
          <h2>Crop Intelligence Dashboard</h2>
          <span>● System Online</span>
        </header>

        {/* Dashboard content */}
        <main className="content">
         

<main className="content">
  <div className="page-heading">
    <div>
      <h1>Welcome to TerraSpectra</h1>
      <p>Hyperspectral Crop Monitoring & Risk Analysis</p>
    </div>

    <span className="demo-label">DEMO DATA</span>
  </div>

  <div className="metrics-grid">

    <div className="metric-card">
      <p>Total Monitored Area</p>
      <h2>{farmSummary.totalArea.toLocaleString()} <span>acres</span></h2>
      <small>Illustrative farm area</small>
    </div>

    <div className="metric-card">
      <p>High-Risk Area</p>
      <h2 className="high-risk">{farmSummary.highRiskArea} <span>acres</span></h2>
      <small>{getHighRiskPercentage()}% of monitored area</small>
      <small>Synthetic risk estimate</small>
    </div>

    <div className="metric-card">
      <p>Monitored Zones</p>
      <h2>{farmSummary.monitoredZones} <span>zones</span></h2>
      <small>Sample monitoring zones</small>
    </div>

  </div>

{/* GIS Map Section */}
<section className="map-section">
  <div className="section-heading">
    <div>
      <h2>Geospatial Risk Overview</h2>
      <p>Farm monitoring and crop stress visualization</p>
    </div>
    <span className="demo-label">SAMPLE MAP</span>
  </div>

  <div className="map-placeholder">
    <div className="map-message">
      <span>GIS MAP</span>
      <h3>Farm Map Visualization</h3>
      <p>Geospatial layers will appear here</p>
      <small>Waiting for GeoJSON farm boundaries</small>
    </div>
  </div>

<div className="risk-legend">
  <h3>Risk Classification</h3>

  
<div className="legend-items">
  {riskData.map((item) => (
    <div className="legend-item" key={item.id}>
      <span className={`risk-dot ${item.className}`}></span>
      {item.label}
    </div>
  ))}
</div>

</div>

</section>

{/* Risk Analytics */}
<section className="analytics-section">
  <h2>Crop Risk Analytics</h2>
  <p className="analytics-subtitle">
    Illustrative distribution across monitored zones
  </p>

  
<div className="analytics-grid">
  {riskData.map((item) => (
    <div className="analytics-card" key={item.id}>
      <span className={`risk-dot ${item.className}`}></span>

      <p>{item.label} Zones</p>

      <h3>{item.zones}</h3>
    </div>
  ))}
</div>

</section>

<section className="chart-section">
  <h2>Risk Distribution</h2>
  <p>Number of zones by risk category · Synthetic demo data</p>

  <div className="chart-container">
    {riskData.map((item) => (
      <div className="chart-row" key={item.label}>
        <span>{item.label}</span>

        <div className="bar-background">
          <div
            className="bar-fill"
            style={{
              width: `${(item.zones / 12) * 100}%`,
              backgroundColor: item.color,
            }}
          ></div>
        </div>

        <strong>{item.zones}</strong>
      </div>
    ))}
  </div>
</section>



</main>


        </main>

      </div>
    </div>
  )
}

export default App

