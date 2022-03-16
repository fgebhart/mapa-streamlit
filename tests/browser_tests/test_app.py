def test_streamlit_app_basic(live_server, webdriver) -> None:
    url = "http://localhost:8501/"
    webdriver.get(url)

    assert webdriver.current_url == url
