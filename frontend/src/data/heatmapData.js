
const zoneGrids = [
  {
    zoneId: 1,
    zoneName: 'Zone A',
    risk: 'Low',
    bounds: [79.940, 23.180, 79.950, 23.190],
    scores: [12, 18, 22, 15],
  },
  {
    zoneId: 2,
    zoneName: 'Zone B',
    risk: 'Medium',
    bounds: [79.952, 23.180, 79.962, 23.190],
    scores: [42, 50, 58, 47],
  },
  {
    zoneId: 3,
    zoneName: 'Zone C',
    risk: 'High',
    bounds: [79.964, 23.180, 79.974, 23.190],
    scores: [76, 82, 88, 91],
  },
]

export const heatmapData = zoneGrids.flatMap((zone) => {
  const [west, south, east, north] = zone.bounds
  const midLon = (west + east) / 2
  const midLat = (south + north) / 2

  const cells = [
    [west, south, midLon, midLat],
    [midLon, south, east, midLat],
    [west, midLat, midLon, north],
    [midLon, midLat, east, north],
  ]

  return cells.map((cell, index) => {
    const [left, bottom, right, top] = cell

    return {
      id: `${zone.zoneName}-P${index + 1}`,
      zoneId: zone.zoneId,
      zoneName: zone.zoneName,
      risk: zone.risk,
      riskScore: zone.scores[index],
      polygon: [
        [left, bottom],
        [right, bottom],
        [right, top],
        [left, top],
        [left, bottom],
      ],
    }
  })
})
