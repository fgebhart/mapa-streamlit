import datetime
import logging
import os
import sys
from pathlib import Path
from typing import List

import folium
import streamlit as st
from folium.plugins import Draw
from mapa import convert_bbox_to_stl
from mapa.caching import get_hash_of_geojson
from mapa.utils import TMPDIR
from streamlit_folium import st_folium

from mapa_streamlit import __version__

log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)

CENTER = [25.0, 55.0]
ZOOM = 3
Z_OFFSET = 2
Z_SCALE = 2.0
AREA_THRESHOLD = 30.0
BTN_LABEL_CREATE_STL = "Create STL"
BTN_LABEL_DOWNLOAD_STL = "Download STL"
MAX_NUMBER_OF_STAC_ITEMS = 20
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


def _show_map(center: List[float], zoom: int) -> folium.Map:
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
    )
    Draw(
        export=False,
        position="topleft",
        draw_options={
            "polyline": False,
            "poly": False,
            "circle": False,
            "polygon": False,
            "marker": False,
            "circlemarker": False,
        },
    ).add_to(m)
    return m


def _compute_stl(folium_output: dict, progress_bar: st.progress):
    if folium_output["last_active_drawing"] is None:
        # this line should never be reached, since the button is deactivated in the given if clause
        st.sidebar.warning("You need to draw a rectangle on the map first!")
    else:
        _cleanup_of_old_stl_files(older_than_n_days=3)
        geometry = folium_output["last_active_drawing"]["geometry"]
        geo_hash = get_hash_of_geojson(geometry)
        path = TMPDIR() / f"{geo_hash}.stl"
        progress_bar.progress(0)
        try:
            convert_bbox_to_stl(
                bbox_geometry=geometry,
                z_scale=Z_SCALE if z_scale is None else z_scale,
                z_offset=Z_OFFSET if z_offset is None else z_offset,
                output_file=path,
                max_number_of_stac_items=MAX_NUMBER_OF_STAC_ITEMS,
                progress_bar=progress_bar,
            )
            # it is important to spawn this success message in the sidebar, because state will get lost otherwise
            st.sidebar.success("Successfully computed STL file!")
        except ValueError:
            st.sidebar.warning(
                "Selected region is too large, fetching data for this area would consume too many resources. "
                "Please select a smaller region."
            )


def _download_btn(data: str, disabled: bool) -> None:
    st.sidebar.download_button(
        label=BTN_LABEL_DOWNLOAD_STL,
        data=data,
        file_name=f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_mapa-streamlit.stl',
        disabled=disabled,
    )


def _cleanup_of_old_stl_files(path: Path = TMPDIR(), older_than_n_days: int = 10) -> None:
    for file in path.iterdir():
        if file.suffix == ".stl":
            creation_ts = os.path.getmtime(file)
            creation_date = datetime.datetime.utcfromtimestamp(creation_ts).date()
            if creation_date >= datetime.datetime.today().date() + datetime.timedelta(days=older_than_n_days):
                log.info(f"file is older than {older_than_n_days} days, deleting it: {file}")
                file.unlink()
            else:
                log.info(f"file not older than {older_than_n_days} days, won't delete it: {file}")


if __name__ == "__main__":
    st.set_page_config(
        page_title="mapa streamlit",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": ABOUT,
        },
    )

    st.markdown(
        """
        # mapa &nbsp; 🌍 &nbsp; Map to STL Converter
        Follow the instructions in the sidebar on the left to create and download a 3D-printable STL file.
        """,
        unsafe_allow_html=True,
    )
    st.write("\n")
    m = _show_map(center=CENTER, zoom=ZOOM)
    output = st_folium(m, key="init", width=1000, height=600)

    geo_hash = None
    if output:
        if output["last_active_drawing"] is not None:
            geometry = output["last_active_drawing"]["geometry"]
            geo_hash = get_hash_of_geojson(geometry)

    # ensure progress bar resides at top of sidebar and is invisible initially
    progress_bar = st.sidebar.progress(0)
    progress_bar.empty()

    # Getting Started container
    with st.sidebar.container():
        st.markdown(
            f"""
            # Getting Started
            1. Click the black square on the map
            2. Draw a rectangle over your region of intereset (The larger the region the longer the STL file creation takes ☝️)
            3. Click on <kbd>{BTN_LABEL_CREATE_STL}</kbd>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            BTN_LABEL_CREATE_STL,
            key="create_stl",
            on_click=_compute_stl,
            kwargs={"folium_output": output, "progress_bar": progress_bar},
            disabled=False if geo_hash else True,
        )
        st.markdown(
            f"""
            4. Wait for the computation to finish
            5. Click on <kbd>{BTN_LABEL_DOWNLOAD_STL}</kbd>
            """,
            unsafe_allow_html=True,
        )

    stl_path = TMPDIR() / f"{geo_hash}.stl"
    if stl_path.is_file():
        with open(stl_path, "rb") as fp:
            _download_btn(fp, False)
    else:
        _download_btn(b"None", True)

    st.sidebar.markdown("---")

    # Customization container
    with st.sidebar.container():
        st.write(
            """
            # Customization
            Use below options to customize the output STL file:
            """
        )
        z_offset = st.slider("z-offset (in millimeter):", 0, 20, Z_OFFSET)
        z_scale = st.slider("z-scale (factor to be multiplied to the z-axis):", 0.0, 5.0, Z_SCALE)
