import datetime
import subprocess
import time
from pathlib import Path

import pytest
from selenium.webdriver import Chrome, ChromeOptions


@pytest.fixture
def webdriver():
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = Chrome(options=options)
    driver.set_window_size(1280, 1024)
    yield driver
    driver.quit()


class LiveServerManager:
    def __init__(self):
        self.process = None

    def __enter__(self):
        self.process = subprocess.Popen(
            ["streamlit", "run", "app.py", "&"], stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL
        )
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.process:
            self.process.terminate()

    @property
    def url(self) -> str:
        return "http://localhost:8501/"


@pytest.fixture
def live_server(webdriver):
    with LiveServerManager() as server:
        # wait a moment for the streamlit server to start up
        time.sleep(5)
        webdriver.get(server.url)
        yield server


@pytest.fixture
def take_screenshot():
    """
    Helper function which is useful when debugging selenium browser tests.
    """

    def _take(webdriver, name: str = None, path: str = None):
        if name is None:
            name = f"{datetime.datetime.now()}_screenshot.png"
        if not name.endswith(".png"):
            name = f"{name}.png"
        if path is None:
            path = Path(__file__).parent.parent.parent / "spike" / "selenium" / "screenshots" / name
        else:
            path = Path(path) / name
        webdriver.save_screenshot(str(path))

    return _take
