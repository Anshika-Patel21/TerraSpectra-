
const riskColors = {
  Low: '#4ade80',
  Medium: '#facc15',
  High: '#fb7185',
}

function RiskChart({ zones }) {
  const categories = ['Low', 'Medium', 'High'].map((risk) => {
    const count = zones.features.filter(
      (feature) => feature.properties.risk === risk
    ).length

    return {
      label: risk,
      zones: count,
      color: riskColors[risk],
    }
  })

  const totalZones = categories.reduce(
    (total, item) => total + item.zones,
    0
  )

  return (
    <section className="chart-section">
      <h2>Risk Distribution</h2>

      <p>Number of visible zones by risk category</p>

      <div className="chart-container">
        {categories.map((item) => (
          <div className="chart-row" key={item.label}>
            <span>{item.label}</span>

            <div className="bar-background">
              <div
                className="bar-fill"
                style={{
                  width: totalZones
                    ? `${(item.zones / totalZones) * 100}%`
                    : '0%',
                  backgroundColor: item.color,
                }}
              ></div>
            </div>

            <strong>{item.zones}</strong>
          </div>
        ))}

        {totalZones === 0 && (
          <p className="no-zone-selected">
            No zones available for this filter.
          </p>
        )}
      </div>
    </section>
  )
}

export default RiskChart

