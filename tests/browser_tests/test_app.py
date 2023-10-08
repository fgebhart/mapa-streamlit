import time
from importlib.metadata import version

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from mapa_streamlit import __version__
from mapa_streamlit.settings import DEFAULT_TILING_FORMAT, ModelSizeSlider, TilingSelect, ZOffsetSlider, ZScaleSlider

DELAY = 3
IGNORED_EXCEPTIONS = (
    NoSuchElementException,
    StaleElementReferenceException,
)


def test_streamlit_app__basic(live_server, webdriver) -> None:
    assert webdriver.current_url == live_server.url
    time.sleep(DELAY)

    h1 = [e.text for e in webdriver.find_elements(By.TAG_NAME, "h1")]
    assert "Getting Started" in h1
    assert "Customization" in h1
    assert "mapa   🌍   Map to STL Converter" in h1

    li = [e.text for e in webdriver.find_elements(By.TAG_NAME, "li")]
    assert "Zoom to your region of interest" in li
    assert "Click the black square on the map" in li
    assert "Draw a rectangle on the map" in li
    assert "Optional: Apply customizations below" in li
    assert "Click on Create STL" in li
    assert "Wait for the computation to finish" in li
    assert "Click on Download STL" in li

    WebDriverWait(webdriver, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
    WebDriverWait(webdriver, DELAY, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.element_to_be_clickable((By.TAG_NAME, "button"))
    )

    buttons = [e.text for e in webdriver.find_elements(By.TAG_NAME, "button")]
    assert "Create STL" in buttons
    assert "Download STL" in buttons

    sliders = [e.text for e in webdriver.find_elements(By.CLASS_NAME, "stSlider")]
    z_offset_slider = sliders[0]
    assert ZOffsetSlider.label in z_offset_slider
    assert str(ZOffsetSlider.max_value) in z_offset_slider
    assert str(ZOffsetSlider.min_value) in z_offset_slider
    assert str(ZOffsetSlider.value) in z_offset_slider

    z_scale_slider = sliders[1]
    assert ZScaleSlider.label in z_scale_slider
    assert str(ZScaleSlider.max_value) in z_scale_slider
    assert str(ZScaleSlider.min_value) in z_scale_slider
    assert str(ZScaleSlider.value) in z_scale_slider

    model_size_slider = sliders[2]
    assert ModelSizeSlider.label in model_size_slider
    assert str(ModelSizeSlider.max_value) in model_size_slider
    assert str(ModelSizeSlider.min_value) in model_size_slider
    assert str(ModelSizeSlider.value) in model_size_slider

    select_box = webdriver.find_element(By.CLASS_NAME, "stSelectbox").text
    assert TilingSelect.label in select_box
    assert DEFAULT_TILING_FORMAT in select_box

    # verify content of about menu
    hamburger = webdriver.find_element(By.CSS_SELECTOR, "#MainMenu > button:nth-child(1) > svg:nth-child(1)")
    hamburger.click()

    element = webdriver.find_element(By.CSS_SELECTOR, "#MainMenu path")
    actions = ActionChains(webdriver)
    actions.move_to_element(element).perform()

    about_xpath = "/html/body/div/div[2]/div/div/div[2]/div/div/div/ul[1]/ul[5]/li/span"
    WebDriverWait(webdriver, DELAY).until(EC.element_to_be_clickable((By.TAG_NAME, "span")))
    WebDriverWait(webdriver, DELAY).until(EC.presence_of_element_located((By.XPATH, about_xpath)))
    WebDriverWait(webdriver, DELAY, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.element_to_be_clickable((By.XPATH, about_xpath))
    )

    about = webdriver.find_element(By.XPATH, about_xpath)
    about.click()
    webdriver.implicitly_wait(DELAY)
    text = [e.text for e in webdriver.find_elements(By.TAG_NAME, "p")]
    about_text = " ".join(text)

    assert f"Made with mapa-streamlit v{__version__}" in about_text
    assert f"Made with mapa v{version('mapa')}" in about_text
    assert "Hi my name is" in about_text
