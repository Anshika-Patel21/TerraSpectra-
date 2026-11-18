
import { riskData } from '../data/riskData'

function RiskChart() {
  const totalZones = riskData.reduce(
    (total, item) => total + item.zones,
    0
  )

  return (
    <section className="chart-section">
      <h2>Risk Distribution</h2>
      <p>Number of zones by risk category · Synthetic demo data</p>

      <div className="chart-container">
        {riskData.map((item) => (
          <div className="chart-row" key={item.id}>
            <span>{item.label}</span>

            <div className="bar-background">
              <div
                className="bar-fill"
                style={{
                  width: `${(item.zones / totalZones) * 100}%`,
                  backgroundColor: item.color,
                }}
              ></div>
            </div>

            <strong>{item.zones}</strong>
          </div>
        ))}
      </div>
    </section>
  )
}

export default RiskChart
