
const riskCategories = [
  { label: 'Low', className: 'risk-low' },
  { label: 'Medium', className: 'risk-medium' },
  { label: 'High', className: 'risk-high' },
]

function RiskAnalytics({ zones }) {
  const analytics = riskCategories.map((category) => {
    const matchingZones = zones.features.filter(
      (feature) => feature.properties.risk === category.label
    )

    const totalArea = matchingZones.reduce(
      (total, feature) => total + feature.properties.area,
      0
    )

    return {
      ...category,
      zones: matchingZones.length,
      area: totalArea,
    }
  })

  return (
    <section className="analytics-section">
      <h2>Crop Risk Analytics</h2>

      <p className="analytics-subtitle">
        Distribution based on the selected risk filter
      </p>

      <div className="analytics-grid">
        {analytics.map((item) => (
          <div className="analytics-card" key={item.label}>
            <span className={`risk-dot ${item.className}`}></span>

            <p>{item.label} Risk Zones</p>

            <h3>{item.zones}</h3>

            <span>{item.area.toLocaleString()} acres</span>
          </div>
        ))}
      </div>
    </section>
  )
}

export default RiskAnalytics

