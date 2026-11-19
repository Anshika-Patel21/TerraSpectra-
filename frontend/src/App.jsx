
import './App.css'
import GISMap from './components/GISMap'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import MetricCard from './components/MetricCard'
import RiskLegend from './components/RiskLegend'
import RiskAnalytics from './components/RiskAnalytics'
import RiskChart from './components/RiskChart'

import {
  farmSummary,
  getHighRiskPercentage,
} from './data/riskData'

function App() {
  return (
    <div className="dashboard">

      <Sidebar />

      <div className="main-area">

        <Header />

        <main className="content">

          {/* Dashboard heading */}
          <div className="page-heading">
            <div>
              <h1>Welcome to TerraSpectra</h1>
              <p>Hyperspectral Crop Monitoring & Risk Analysis</p>
            </div>

            <span className="demo-label">
              DEMO DATA
            </span>
          </div>

          {/* KPI Metric Cards */}
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

          {/* GIS Map */}
          <section className="map-section">

            <div className="section-heading">
              <div>
                <h2>Geospatial Risk Overview</h2>
                <p>
                  Farm monitoring and crop stress visualization
                </p>
              </div>

              <span className="demo-label">
                SAMPLE MAP
              </span>
            </div>

           <GISMap />

            <RiskLegend />

          </section>

          {/* Analytics */}
          <RiskAnalytics />

          {/* Risk Distribution Chart */}
          <RiskChart />

        </main>
      </div>
    </div>
  )
}

export default App


