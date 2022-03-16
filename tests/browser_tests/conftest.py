import subprocess
import time

import pytest
from selenium.webdriver import Chrome, ChromeOptions


@pytest.fixture
def webdriver():
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(options=options)
    driver.set_window_size(1280, 1024)
    yield driver
    driver.quit()


@pytest.fixture
def live_server():
    proc = subprocess.Popen(["streamlit", "run", "app.py", "&"])
    # wait a moment for the streamlit server to start up
    time.sleep(1)
    yield
    # once test is finished, kill streamlit process
    proc.kill()
