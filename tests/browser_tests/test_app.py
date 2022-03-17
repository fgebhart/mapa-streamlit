import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from mapa_streamlit import __version__
from mapa_streamlit.settings import ZOffsetSlider, ZScaleSlider

TIMEOUT = 3
IGNORED_EXCEPTIONS = (
    NoSuchElementException,
    StaleElementReferenceException,
)


def test_streamlit_app__basic(live_server, webdriver) -> None:
    assert webdriver.current_url == live_server.url
    time.sleep(1)

    h1 = [e.text for e in webdriver.find_elements(By.TAG_NAME, "h1")]
    assert "Getting Started" in h1
    assert "Customization" in h1
    assert "mapa   🌍   Map to STL Converter" in h1

    li = [e.text for e in webdriver.find_elements(By.TAG_NAME, "li")]
    assert "Click the black square on the map" in li
    assert (
        "Draw a rectangle over your region of intereset "
        "(The larger the region the longer the STL file creation takes ☝️)" in li
    )
    assert "Click on Create STL" in li
    assert "Wait for the computation to finish" in li
    assert "Click on Download STL" in li

    WebDriverWait(webdriver, TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
    WebDriverWait(webdriver, TIMEOUT, ignored_exceptions=IGNORED_EXCEPTIONS).until(
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

    # verify content of about menu
    hamburger = webdriver.find_element(By.CSS_SELECTOR, "#MainMenu > button:nth-child(1) > svg:nth-child(1)")
    hamburger.click()

    element = webdriver.find_element(By.CSS_SELECTOR, "#MainMenu path")
    actions = ActionChains(webdriver)
    actions.move_to_element(element).perform()

    about_xpath = "/html/body/div/div[2]/div/div/div[3]/div/div/ul[1]/ul[6]/li/span"
    WebDriverWait(webdriver, TIMEOUT).until(EC.element_to_be_clickable((By.TAG_NAME, "span")))
    WebDriverWait(webdriver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, about_xpath)))
    WebDriverWait(webdriver, TIMEOUT, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.element_to_be_clickable((By.XPATH, about_xpath))
    )

    about = webdriver.find_element(By.XPATH, about_xpath)
    about.click()
    webdriver.implicitly_wait(3)
    text = [e.text for e in webdriver.find_elements(By.TAG_NAME, "p")]
    about_text = " ".join(text)

    assert f"Made with mapa-streamlit v{__version__}" in about_text
    assert "Hi my name is" in about_text


def test_streamlit_app__functionality(live_server, webdriver, take_screenshot) -> None:
    assert webdriver.current_url == live_server.url
    time.sleep(1)

    # TODO verify that "CREATE STL" button is disabled
    # TODO verify that "DOWNLOAD STL" button is disabled
    # webdriver.implicitly_wait(3)
    # click draw rect icon on folium map
    take_screenshot(webdriver, "after_page_load")
    webdriver.switch_to.frame(0)
    rect_button = webdriver.find_element(By.CLASS_NAME, "leaflet-draw-draw-rectangle")
    rect_button.click()

    take_screenshot(webdriver, "clicked_rect_button")

    # webdriver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(webdriver, 20).until(EC.vi
    # sibility_of_element_located((By.XPATH, "//h2[text()='Interactive Choropleth Map']"))))
    # WebDriverWait(webdriver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"div.css-6wrhc:nt
    # h-child(3) > iframe:nth-child(1)")))
    # take_screenshot(webdriver, "switched_to_iframe")
    # elements = webdriver.find_elements_by_css_selector("svg.leaflet-zoom-animated>g path")
    # for element in elements:
    #     ActionChains(webdriver).move_to_element(element).perform()
    #     print(WebDriverWait(webdriver, 3).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='info lea
    # flet-control']"))).text)

    leaflet_map = webdriver.find_element(By.ID, "map_div")
    webdriver.switch_to.default_content()
    time.sleep(1)
    take_screenshot(webdriver, "switched_to_default_content")
    draw_rect = ActionChains(webdriver).move_to_element_with_offset(leaflet_map, 20, 20)
    draw_rect.click_and_hold()
    draw_rect = ActionChains(webdriver).move_to_element_with_offset(leaflet_map, 200, 200)
    draw_rect.release()
    draw_rect.perform()

    time.sleep(1)
    breakpoint()
