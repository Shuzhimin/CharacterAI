from app.common.image_to_url import upload_file, get_url


def test_upload_file() -> None:
    upload_file(image_path='app/common/character_form.png')
    print("upload_file is successful")


def test_get_url() -> None:
    url = get_url()
    print(url)