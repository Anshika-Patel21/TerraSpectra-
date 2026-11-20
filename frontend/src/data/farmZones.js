
export const farmZones = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: {
        id: 1,
        name: 'Zone A',
        risk: 'Low',
        area: 350,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [79.940, 23.180],
          [79.950, 23.180],
          [79.950, 23.190],
          [79.940, 23.190],
          [79.940, 23.180],
        ]],
      },
    },
    {
      type: 'Feature',
      properties: {
        id: 2,
        name: 'Zone B',
        risk: 'Medium',
        area: 605,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [79.952, 23.180],
          [79.962, 23.180],
          [79.962, 23.190],
          [79.952, 23.190],
          [79.952, 23.180],
        ]],
      },
    },
    {
      type: 'Feature',
      properties: {
        id: 3,
        name: 'Zone C',
        risk: 'High',
        area: 45,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [79.964, 23.180],
          [79.974, 23.180],
          [79.974, 23.190],
          [79.964, 23.190],
          [79.964, 23.180],
        ]],
      },
    },
  ],
}

