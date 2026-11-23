
import { farmAnalytics } from '../data/analyticsData'

function FarmSummary() {
  const { totalArea, lowRiskArea, mediumHighRiskArea } = farmAnalytics

  const metrics = [
    {
      label: 'Total Farm Area',
      value: totalArea,
      color: 'summary-total',
    },
    {
      label: 'Low-Risk Area',
      value: lowRiskArea,
      color: 'summary-healthy',
    },
    {
      label: 'Medium/High-Risk Area',
      value: mediumHighRiskArea,
      color: 'summary-stressed',
    },
  ]

  return (
    <section className="farm-summary-section">
      <div className="section-heading">
        <div>
          <h2>Farm Area Summary</h2>
          <p>Overall acreage distribution across the monitored farm</p>
        </div>

        <span className="demo-label">SYNTHETIC DATA</span>
      </div>

      <div className="farm-summary-grid">
        {metrics.map((metric) => (
          <div className="farm-summary-card" key={metric.label}>
            <p>{metric.label}</p>
            <h3 className={metric.color}>
              {metric.value.toLocaleString()}
              <span> acres</span>
            </h3>
          </div>
        ))}
      </div>
    </section>
  )
}

export default FarmSummary

