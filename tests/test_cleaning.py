from mapa_streamlit.cleaning import (
    _delete_files_in_dir,
    _get_data_size_of_dir,
    _get_disk_usage,
    _get_number_of_files_in_dir,
    run_cleanup_job,
)


def test__get_disk_usage():
    usage = _get_disk_usage()
    assert isinstance(usage, float)
    assert 0.0 < usage <= 100.0


def test__get_data_size_of_dir(tmp_path):
    # get size of empty dir
    size = _get_data_size_of_dir(tmp_path)
    assert size == 0

    # put dummy file into dir
    file_1_size = 1234
    file_1 = tmp_path / "file_1.stl"
    f = open(file_1, "wb")
    f.seek(file_1_size - 1)
    f.write(b"\0")
    f.close()

    size = _get_data_size_of_dir(tmp_path)
    assert size == round(file_1_size / 1024**2, 4)

    # put another file into the dir
    file_2_size = 2345
    file_2 = tmp_path / "file_2.stl"
    f = open(file_2, "wb")
    f.seek(file_2_size - 1)
    f.write(b"\0")
    f.close()

    size = _get_data_size_of_dir(tmp_path)
    assert size == round((file_1_size + file_2_size) / 1024**2, 4)

    # verify files in nested dirs are also taken into account
    file_3_size = 3456
    d = tmp_path / "sub"
    d.mkdir()
    file_3 = d / "file_3.stl"
    f = open(file_3, "wb")
    f.seek(file_3_size - 1)
    f.write(b"\0")
    f.close()

    size = _get_data_size_of_dir(tmp_path)
    assert size == round((file_1_size + file_2_size + file_3_size) / 1024**2, 4)


def test__delete_files_in_dir(tmp_path) -> None:
    # verify function deletes stl file
    p = tmp_path / "baa.stl"
    p.write_text("foo")
    assert p.is_file()
    _delete_files_in_dir(tmp_path, ".stl")
    assert not p.is_file()

    # running it again does not fail
    _delete_files_in_dir(tmp_path, ".stl")

    # ensure files beside stl files won't be deleted
    p = tmp_path / "baa.tiff"
    p.write_text("foo")
    assert p.is_file()
    _delete_files_in_dir(tmp_path, ".stl")
    assert p.is_file()


def test__get_number_of_files_in_dir(tmp_path) -> None:
    num = _get_number_of_files_in_dir(tmp_path, ".stl")
    assert num == 0

    stl = tmp_path / "baa.stl"
    stl.write_text("foo")
    num = _get_number_of_files_in_dir(tmp_path, ".stl")
    assert num == 1
    num = _get_number_of_files_in_dir(tmp_path, ".tiff")
    assert num == 0

    tiff = tmp_path / "baa.tiff"
    tiff.write_text("foo")
    num = _get_number_of_files_in_dir(tmp_path, ".stl")
    assert num == 1
    num = _get_number_of_files_in_dir(tmp_path, ".tiff")
    assert num == 1


def test_run_cleanup_job(tmp_path) -> None:
    # chose very low threshold to ensure files will be delted
    stl = tmp_path / "baa.stl"
    stl.write_text("foo")
    assert stl.is_file()
    tiff = tmp_path / "baa.tiff"
    tiff.write_text("foo")
    assert tiff.is_file()
    zip = tmp_path / "baz.zip"
    zip.write_text("foo")
    assert zip.is_file()

    run_cleanup_job(tmp_path, disk_cleaning_threshold=0.0)
    assert not stl.is_file()
    assert tiff.is_file()
    assert not zip.is_file()

    # chose very high threshold to check that files won't get deleted
    stl = tmp_path / "baa.stl"
    stl.write_text("foo")
    assert stl.is_file()
    tiff = tmp_path / "baa.tiff"
    tiff.write_text("foo")
    assert tiff.is_file()

    run_cleanup_job(tmp_path, disk_cleaning_threshold=100.0)
    assert stl.is_file()
    assert tiff.is_file()
