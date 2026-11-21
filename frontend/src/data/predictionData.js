
export const predictionData = [
  {
    zoneId: 1,
    disease: 'Early Blight',
    risk: 'Low',
    riskScore: 12,
    confidence: 91,
    affectedArea: 8,
    forecast: [12, 15, 18],
  },
  {
    zoneId: 2,
    disease: 'Early Blight',
    risk: 'Medium',
    riskScore: 48,
    confidence: 87,
    affectedArea: 96,
    forecast: [48, 55, 63],
  },
  {
    zoneId: 3,
    disease: 'Early Blight',
    risk: 'High',
    riskScore: 82,
    confidence: 94,
    affectedArea: 37,
    forecast: [82, 86, 91],
  },
]

export const getPredictionByZone = (zoneId) =>
  predictionData.find((item) => item.zoneId === zoneId)
