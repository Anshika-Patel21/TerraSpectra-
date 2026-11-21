
import { predictionData } from '../data/predictionData'

function PredictionOverview({ zones }) {
  const visiblePredictions = predictionData.filter((prediction) =>
    zones.features.some(
      (feature) => feature.properties.id === prediction.zoneId
    )
  )

  const averageRisk = visiblePredictions.length
    ? Math.round(
        visiblePredictions.reduce(
          (total, item) => total + item.riskScore,
          0
        ) / visiblePredictions.length
      )
    : 0

  const highRiskZones = visiblePredictions.filter(
    (item) => item.risk === 'High'
  ).length

  return (
    <section className="prediction-section">
      <div className="prediction-heading">
        <div>
          <h2>Disease Prediction Overview</h2>
          <p>Illustrative early blight risk estimates</p>
        </div>
        <span className="demo-label">SYNTHETIC DATA</span>
      </div>

      <div className="prediction-grid">
        <div className="prediction-card">
          <p>Zones Analysed</p>
          <h3>{visiblePredictions.length}</h3>
          <span>Visible zones</span>
        </div>

        <div className="prediction-card">
          <p>Average Risk Score</p>
          <h3>{averageRisk}%</h3>
          <span>Illustrative risk index</span>
        </div>

        <div className="prediction-card">
          <p>High-Risk Zones</p>
          <h3>{highRiskZones}</h3>
          <span>Within current filter</span>
        </div>
      </div>
    </section>
  )
}

export default PredictionOverview
