from mapa_streamlit import __version__
from mapa_streamlit.app import _cleanup_of_old_stl_files


def test_version():
    assert __version__ == "0.1.0"


def test__cleanup_of_old_stl_files(tmp_path):
    # verify file gets deleted
    p = tmp_path / "baa.stl"
    p.write_text("foo")
    assert p.is_file()
    _cleanup_of_old_stl_files(tmp_path, older_than_n_days=0)
    assert not p.is_file()

    # file should not get deleted
    p = tmp_path / "baa.stl"
    p.write_text("foo")
    assert p.is_file()
    _cleanup_of_old_stl_files(tmp_path, older_than_n_days=1)
    assert p.is_file()
