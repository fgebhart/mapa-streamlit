from mapa_streamlit import __version__

MAP_CENTER = [25.0, 55.0]
MAP_ZOOM = 3

BTN_LABEL_CREATE_STL = "Create STL"
BTN_LABEL_DOWNLOAD_STL = "Download STL"

MAX_ALLOWED_AREA_SIZE = 25.0

DISK_CLEANING_THRESHOLD = 60.0

ABOUT = f"""
# mapa 🌍
Hi my name is Fabian Gebhart :wave: and I am the author of mapa. mapa let's you create 3D-printable STL files
from every region around the globe. The elevation data is retrieved from
[ALOS DEM hosted by MS Planetary Computer](https://planetarycomputer.microsoft.com/dataset/alos-dem), which provides
satellite data with 30m resolution.
If you want to reach out, follow me or report a bug, you can do so via
[Github](https://github.com/fgebhart) or [Twitter](https://twitter.com/FabianGebhart).
For more details please refer to:
* the [mapa-streamlit repo](https://github.com/fgebhart/mapa-streamlit) which contains the source code of this streamlit app or
* the original [mapa repo](https://github.com/fgebhart/mapa) which contains the source code of the [mapa python package](https://pypi.org/project/mapa/)
Made with mapa-streamlit v{__version__}
"""

MAPA_SHINES_AT = """
Mapa shines at generating 3d models of particular regions, mountains or cities. Generating 3d models of e.g. entire continents is currently not supported.
"""

DEFAULT_Z_OFFSET = 2
DEFAULT_Z_SCALE = 2.0


class ZOffsetSlider:
    label: str = "z-offset (in millimeter):"
    min_value: int = 0
    max_value: int = 20
    value: int = DEFAULT_Z_OFFSET


class ZScaleSlider:
    label: str = "z-scale (factor to be multiplied to the z-axis):"
    min_value: int = 0.0
    max_value: int = 5.0
    value: int = DEFAULT_Z_SCALE
