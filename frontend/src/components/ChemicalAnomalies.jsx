
import { chemicalAnomalies } from '../data/anomalyData'

function ChemicalAnomalies() {
  const affectedZones = new Set(
    chemicalAnomalies.flatMap((item) => item.affectedZones)
  ).size

  const severityClass = {
    High: 'anomaly-high',
    Medium: 'anomaly-medium',
    Low: 'anomaly-low',
  }

  return (
    <section className="anomaly-section">
      <div className="section-heading">
        <div>
          <h2>Spectral Anomaly Indicators</h2>
          <p>Illustrative vegetation and nutrient-related deviations</p>
        </div>

        <span className="demo-label">SYNTHETIC DATA</span>
      </div>

      <div className="anomaly-summary">
        <div className="anomaly-summary-card">
          <p>Detected Indicators</p>
          <h3>{chemicalAnomalies.length}</h3>
        </div>

        <div className="anomaly-summary-card">
          <p>Affected Zones</p>
          <h3>{affectedZones}</h3>
        </div>
      </div>

      <div className="anomaly-list">
        {chemicalAnomalies.map((item) => (
          <div className="anomaly-card" key={item.id}>
            <div className="anomaly-card-header">
              <h3>{item.indicator}</h3>

              <span className={severityClass[item.severity]}>
                {item.severity} Severity
              </span>
            </div>

            <p>{item.description}</p>

            <div className="anomaly-zones">
              <span>Affected zones:</span>
              <strong>{item.affectedZones.join(', ')}</strong>
            </div>
          </div>
        ))}
      </div>

      <p className="forecast-note">
        These are illustrative spectral indicators, not validated chemical
        measurements or actual model detections.
      </p>
    </section>
  )
}

export default ChemicalAnomalies
