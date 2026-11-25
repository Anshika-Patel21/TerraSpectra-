
function MetricCard({ title, value, unit, description, variant }) {
  return (
    <div className="metric-card">
      <p>{title}</p>

      <h2 className={variant}>
        {value} <span>{unit}</span>
      </h2>

      <small>{description}</small>
    </div>
  )
}

export default MetricCard
