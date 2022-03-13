import datetime
from pathlib import Path
from typing import List
import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
from mapa import convert_bbox_to_stl
from mapa.caching import get_hash_of_geojson


CENTER = [40.5566, 23.4660]
ZOOM = 4


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


def _compute_stl(folium_output: dict):
    if folium_output["last_active_drawing"] is None:
        st.sidebar.error("You need to draw a rectangle on the map first!")
    else:
        geometry = folium_output["last_active_drawing"]["geometry"]
        geo_hash = get_hash_of_geojson(geometry)
        print(f"hash of geojson: {geo_hash}")
        # with st.spinner("Computing STL file... Please wait... "):
        # TODO check that area of geometry is smaller than ......
        path = Path(__file__).parent / f"{geo_hash}.stl"
        convert_bbox_to_stl(geometry, output_file=path)
        st.sidebar.success("Finished computing STL file! 🎈")


# run app
st.write(
    """
    # mapa 🌍 - Map to STL Converter
    Create and download 3D-printable STL files from around the globe.
    """
)
st.write("\n")
m = _show_map(center=CENTER, zoom=ZOOM)
output = st_folium(m, key="init", width=800, height=600)


geo_hash = None
if output:
    if output["last_active_drawing"] is not None:
        geometry = output["last_active_drawing"]["geometry"]
        geo_hash = get_hash_of_geojson(geometry)

st.sidebar.write(
    """
    # Getting Started

    1. Click the black square on the map
    2. Draw a rectangle over your region of intereset
    3. Click on "Create 3D Model"
    """
)

st.sidebar.button(
    "Create STL",
    key="create_3d_model",
    help=None,
    on_click=_compute_stl,
    args=None,
    kwargs={
        "folium_output": output,
    },
    disabled=False if geo_hash else True,
)

st.sidebar.write(
    """
    4. Wait for the computation to finish
    5. Click on "Download STL"
    """
)


def _download_btn(data, disabled):
    st.sidebar.download_button(
        label="Download STL",
        data=data,
        file_name=f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_mapa-streamlit.stl',
        disabled=disabled,
    )


if geo_hash:
    path = Path(__file__).parent / f"{geo_hash}.stl"
    if path.is_file():
        with open(path, "rb") as fp:
            _download_btn(fp, False)
    else:
        _download_btn(b"None", True)
else:
    _download_btn(b"None", True)
