
export const riskData = [
  {
    id: 1,
    label: 'Low Risk',
    zones: 6,
    color: '#4ade80',
    className: 'low',
  },
  {
    id: 2,
    label: 'Medium Risk',
    zones: 4,
    color: '#facc15',
    className: 'medium',
  },
  {
    id: 3,
    label: 'High Risk',
    zones: 2,
    color: '#fb7185',
    className: 'high',
  },
]

export const farmSummary = {
  totalArea: 1000,
  highRiskArea: 45,
  monitoredZones: 12,
  dataType: 'SYNTHETIC DEMO DATA',
}

export const getHighRiskPercentage = () => {
  return (
    (farmSummary.highRiskArea / farmSummary.totalArea) * 100
  ).toFixed(1)
}
