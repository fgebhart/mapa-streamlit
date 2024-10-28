# mapa-streamlit 🌍

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://3dmaps.streamlitapp.com)
[![Python Tests](https://github.com/fgebhart/mapa-streamlit/actions/workflows/test.yml/badge.svg)](https://github.com/fgebhart/mapa-streamlit/actions/workflows/test.yml)

A [streamlit web app](https://3dmaps.streamlitapp.com) which let's you create 3D-printable
STL files using satellite elevation data ([ALOS DEM](https://planetarycomputer.microsoft.com/dataset/alos-dem)) based on
[mapa](https://github.com/fgebhart/mapa).

This repo contains the source code of the streamlit web app, whereas the
[mapa repository](https://github.com/fgebhart/mapa) contains the source code of the algorithm which is responsible for
generating STL files.

![](https://i.imgur.com/WRwXpeE.png)


## Development & Contributions

Contributions are welcome! In case you would like to contribute to the
[mapa python package](https://pypi.org/project/mapa/), have a look at the
[mapa repository](https://github.com/fgebhart/mapa).

For setting up the development environment, clone this repo

```shell
git clone git@github.com:fgebhart/mapa-streamlit.git && cd mapa-streamlit
```

and run the following commands to install the requirements (in case you don't have poetry install, you can do so with
`pip install poetry`):

```shell
poetry install
poetry shell
```

To run the tests, run:

```shell
pytest tests/
```

To run the streamlit app, run:

```shell
streamlit run app.py
```
