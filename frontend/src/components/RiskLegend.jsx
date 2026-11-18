
import { riskData } from '../data/riskData'

function RiskLegend() {
  return (
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
  )
}

export default RiskLegend
