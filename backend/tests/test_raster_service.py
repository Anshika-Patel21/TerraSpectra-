import unittest
import tempfile
import numpy as np
import rasterio

from pathlib import Path
from rasterio.transform import from_origin
from app.services.raster_service import inspect_raster


class TestRasterService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.raster_path = Path(self.temp_dir.name) / "test_raster.tif"

        with rasterio.open(
            self.raster_path,
            "w",
            driver="GTiff",
            width=10,
            height=5,
            count=2,
            dtype="uint8",
            crs="EPSG:4326",
            transform=from_origin(0, 10, 2, 2)
        ) as dst:

            dst.write(np.ones((5, 10), dtype="uint8"), 1)
            dst.write(np.ones((5, 10), dtype="uint8"), 2)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_raster(self):
        metadata = inspect_raster(str(self.raster_path))

        self.assertEqual(metadata["width"], 10)
        self.assertEqual(metadata["height"], 5)
        self.assertEqual(metadata["band_count"], 2)

    def test_raster_resolution(self):
        metadata = inspect_raster(str(self.raster_path))

        self.assertEqual(metadata["resolution"]["x"], 2)
        self.assertEqual(metadata["resolution"]["y"], 2)

    def test_raster_crs(self):
        metadata = inspect_raster(str(self.raster_path))

        self.assertEqual(metadata["crs"], "EPSG:4326")

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            inspect_raster("missing_raster.tif")

    def test_invalid_file(self):
        invalid_path = Path(self.temp_dir.name) / "invalid.tif"
        invalid_path.write_text("This is not a valid raster")

        with self.assertRaises(ValueError):
            inspect_raster(str(invalid_path))


if __name__ == "__main__":
    unittest.main()