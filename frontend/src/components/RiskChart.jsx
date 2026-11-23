
import { farmAnalytics } from '../data/analyticsData'

const riskColors = {
  Low: '#4ade80',
  Medium: '#facc15',
  High: '#fb7185',
}

function RiskChart() {
  const categories = farmAnalytics.riskDistribution

  return (
    <section className="chart-section">
      <h2>Risk Distribution by Area</h2>

      <p>Share of total monitored acreage in each risk category</p>

      <div className="chart-container">
        {categories.map((item) => {
          const percentage = (
            (item.area / farmAnalytics.totalArea) * 100
          ).toFixed(1)

          return (
            <div className="chart-row" key={item.risk}>
              <span>{item.risk}</span>

              <div className="bar-background">
                <div
                  className="bar-fill"
                  style={{
                    width: `${percentage}%`,
                    backgroundColor: riskColors[item.risk],
                  }}
                />
              </div>

              <strong>{percentage}%</strong>
            </div>
          )
        })}
      </div>

      <p className="forecast-note">
        Acreage distribution is based on synthetic demo data.
      </p>
    </section>
  )
}

export default RiskChart


