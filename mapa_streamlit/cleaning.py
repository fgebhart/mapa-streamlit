import logging
import shutil
from pathlib import Path
from typing import Union

import psutil

log = logging.getLogger(__name__)


def _get_disk_usage(path: Path = ".") -> float:
    """Returns the current disk usage of the given path in percentages.

    Parameters
    ----------
    path : Path, optional
        Path for which the disk usage should be determined, by default "."

    Returns
    -------
    float
        Value between 0.0 and 100.0 percent. 0.0 means disk is empty, 100.0 means disk is full.
    """

    stat = shutil.disk_usage(path)
    return round(stat.used / stat.total * 100.0, 2)


def _get_ram_usage() -> float:
    return psutil.virtual_memory().percent


def _get_data_size_of_dir(path: Path) -> float:
    """Returns the data volume / size of a directory given at path.

    Parameters
    ----------
    path : Path
        Path for which the size should be determined

    Returns
    -------
    float
        Value between 0 and the max size of your disk in mega bytes.
    """

    return round(sum(f.stat().st_size for f in path.glob("**/*") if f.is_file()) / 1024**2, 4)


def _delete_files_in_dir(path: Path, file_suffix: str, name_prefix: Union[None, str] = None) -> None:
    for file in path.iterdir():
        if file.suffix == file_suffix:
            if name_prefix:  # if name prefix is specified, only delete file if name matches
                if file.name.startswith(name_prefix):
                    file.unlink()
                    log.info(f"🗑  deleted file: {file}")
            else:
                file.unlink()
                log.info(f"🗑  deleted file: {file}")


def _get_number_of_files_in_dir(path: Path, file_suffix: str) -> int:
    return len([f for f in path.glob("**/*") if f.suffix == file_suffix])


def run_cleanup_job(path: Path, disk_cleaning_threshold: float) -> None:
    disk_usage = _get_disk_usage(path)
    ram_usage = _get_ram_usage()
    mapa_cache = _get_data_size_of_dir(path)
    log.info(f"💾  Disk usage: {disk_usage}%, Ram usage: {ram_usage}%, mapa files: {mapa_cache} MB")
    stl_num = _get_number_of_files_in_dir(path, ".stl")
    tiff_num = _get_number_of_files_in_dir(path, ".tiff")
    log.info(f"🗂  Number of STL files: {stl_num}, number of TIFF files: {tiff_num}")
    if disk_usage > disk_cleaning_threshold:
        log.info(f"🧹  Disk usage exceeds threshold ({disk_usage}%>{disk_cleaning_threshold}%), deleting files ...")
        _delete_files_in_dir(path, ".stl")
        _delete_files_in_dir(path, ".zip")
        _delete_files_in_dir(path, ".tiff", name_prefix="merged_")
        _delete_files_in_dir(path, ".tiff", name_prefix="clipped_")
    else:
        log.info(
            f"✅  Disk usage does not exceed threshold ({disk_usage}%<{disk_cleaning_threshold}%), no cleaning required."
        )
