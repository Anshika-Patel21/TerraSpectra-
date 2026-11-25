
import { farmAnalytics } from '../data/analyticsData'

function RiskAnalytics() {
  return (
    <section className="analytics-section">
      <h2>Crop Risk Analytics</h2>

      <p className="analytics-subtitle">
        Farm-wide distribution by risk category
      </p>

      <div className="analytics-grid">
        {farmAnalytics.riskDistribution.map((item) => (
          <div className="analytics-card" key={item.risk}>
            <span className={`risk-dot risk-${item.risk.toLowerCase()}`} />

            <p>{item.risk} Risk Zones</p>

            <h3>{item.zones}</h3>

            <span>{item.area.toLocaleString()} acres</span>
          </div>
        ))}
      </div>

      <p className="forecast-note">
        Risk distribution is based on synthetic demo data.
      </p>
    </section>
  )
}

export default RiskAnalytics


