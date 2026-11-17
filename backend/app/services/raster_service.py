import rasterio
from pathlib import Path
from rasterio.errors import RasterioIOError


def inspect_raster(file_path: str):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Raster file not found")

    try:
        with rasterio.open(path) as src:

            metadata = {
                "file_name": path.name,
                "width": src.width,
                "height": src.height,
                "band_count": src.count,
                "crs": str(src.crs) if src.crs else None,
                "resolution": {
                    "x": abs(src.transform.a),
                    "y": abs(src.transform.e)
                },
                "data_types": list(src.dtypes),
                "no_data_value": src.nodata
            }

            return metadata

    except RasterioIOError:
        raise ValueError("Invalid or unsupported raster file")