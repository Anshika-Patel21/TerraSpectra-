
import { riskData } from '../data/riskData'

function RiskAnalytics() {
  return (
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
  )
}

export default RiskAnalytics
