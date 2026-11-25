
import { predictionData } from '../data/predictionData'

function ForecastChart({ zones }) {
  const visiblePredictions = predictionData.filter((prediction) =>
    zones.features.some(
      (feature) => feature.properties.id === prediction.zoneId
    )
  )

  const weeks = ['Week 1', 'Week 2', 'Week 3']

  const averageForecast = weeks.map((week, index) => {
    if (!visiblePredictions.length) {
      return { week, score: 0 }
    }

    const total = visiblePredictions.reduce(
      (sum, item) => sum + item.forecast[index],
      0
    )

    return {
      week,
      score: Math.round(total / visiblePredictions.length),
    }
  })

  return (
    <section className="forecast-section">
      <h2>Three-Week Disease Risk Forecast</h2>
      <p>Illustrative average risk trend across visible zones</p>

      <div className="forecast-chart">
        {averageForecast.map((item) => (
          <div className="forecast-item" key={item.week}>
            <div className="forecast-value">{item.score}%</div>

            <div className="forecast-bar-track">
              <div
                className="forecast-bar-fill"
                style={{ height: `${item.score}%` }}
              />
            </div>

            <span>{item.week}</span>
          </div>
        ))}
      </div>

      <p className="forecast-note">
        Forecast values are synthetic and do not represent validated model output.
      </p>
    </section>
  )
}

export default ForecastChart
