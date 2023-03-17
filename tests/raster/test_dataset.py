from typing import List
import os
import numpy as np
from osgeo import gdal
from pyramids.raster import Raster, Dataset


class TestReadDataset:
    def test_read_all_without_order(
        self,
        rasters_folder_path: str,
        rasters_folder_rasters_number: int,
        rasters_folder_dim: tuple,
    ):
        dataset = Dataset.read_separate_files(rasters_folder_path, with_order=False)
        assert isinstance(dataset.raster, gdal.Dataset)
        assert dataset.no_data_value[0] == 2147483648.0
        assert isinstance(dataset.files, list)
        assert dataset.time_lenth == rasters_folder_rasters_number
        assert dataset.rows == rasters_folder_dim[0]
        assert dataset.columns == rasters_folder_dim[1]

    def test_read_all_with_order(
        self,
        rasters_folder_path: str,
        rasters_folder_rasters_number: int,
        rasters_folder_dim: tuple,
    ):
        dataset = Dataset.read_separate_files(rasters_folder_path, with_order=True)
        assert isinstance(dataset.raster, gdal.Dataset)
        assert dataset.no_data_value[0] == 2147483648.0
        assert isinstance(dataset.files, list)
        assert dataset.time_lenth == rasters_folder_rasters_number
        assert dataset.rows == rasters_folder_dim[0]
        assert dataset.columns == rasters_folder_dim[1]

    def test_read_between_dates(
        self,
        rasters_folder_path: str,
        rasters_folder_start_date: str,
        rasters_folder_end_date: str,
        rasters_folder_date_fmt: str,
        rasters_folder_dim: tuple,
        rasters_folder_between_dates_raster_number: int,
    ):
        dataset = Dataset.read_separate_files(
            rasters_folder_path,
            with_order=True,
            start=rasters_folder_start_date,
            end=rasters_folder_end_date,
            fmt=rasters_folder_date_fmt,
        )
        assert isinstance(dataset.raster, gdal.Dataset)
        assert dataset.no_data_value[0] == 2147483648.0
        assert isinstance(dataset.files, list)
        assert dataset.time_lenth == rasters_folder_between_dates_raster_number
        assert dataset.rows == rasters_folder_dim[0]
        assert dataset.columns == rasters_folder_dim[1]

    # def test_from_netcdf(nc_path: str):
    #     Dataset.readNC(nc_path, "", separator="_")

class TestAscii:
    def test_read_all_without_order(
        self,
        ascii_folder_path: str,
        rasters_folder_rasters_number: int,
        rasters_folder_dim: tuple,
    ):
        dataset = Dataset.read_separate_files(ascii_folder_path, with_order=False, extension=".asc")
        assert isinstance(dataset.raster, gdal.Dataset)
        assert dataset.no_data_value[0] == 2147483648.0
        assert isinstance(dataset.files, list)
        assert dataset.time_lenth == rasters_folder_rasters_number
        assert dataset.rows == rasters_folder_dim[0]
        assert dataset.columns == rasters_folder_dim[1]

class TestReadArray:
    def test_geotiff(
            self,
            rasters_folder_path: str,
            rasters_folder_rasters_number: int,
            rasters_folder_dim: tuple,
    ):
        dataset = Dataset.read_separate_files(rasters_folder_path, with_order=False)
        arr = dataset.read_array()
        assert arr.shape == (
            rasters_folder_rasters_number,
            rasters_folder_dim[0],
            rasters_folder_dim[1],
        )

    def test_ascii(
            self,
            ascii_folder_path: str,
            rasters_folder_rasters_number: int,
            rasters_folder_dim: tuple,
    ):
        dataset = Dataset.read_separate_files(ascii_folder_path, with_order=False, extension=".asc")
        arr = dataset.read_array()
        assert arr.shape == (
            rasters_folder_rasters_number,
            rasters_folder_dim[0],
            rasters_folder_dim[1],
        )


def test_crop_folder(
    src: Dataset,
    crop_aligned_folder_path: str,
    crop_aligned_folder_saveto: str,
):
    Dataset.crop_aligned(crop_aligned_folder_path, src, crop_aligned_folder_saveto)
    assert len(os.listdir(crop_aligned_folder_saveto)) == 3


def test_merge(
    merge_input_raster: List[str],
    merge_output: str,
):
    Dataset.gdal_merge(merge_input_raster, merge_output)
    assert os.path.exists(merge_output)
    src = gdal.Open(merge_output)
    assert src.GetRasterBand(1).GetNoDataValue() == 0
