from unittest.mock import patch

from PIL import Image

from src.scripts import convert_images_to_webp as script


def test_convert_and_delete_reports_missing_directory(capsys):
    script.convert_and_delete("missing-dir", quality=80)

    assert "does not exist" in capsys.readouterr().out


def test_convert_and_delete_converts_supported_images_and_deletes_original(tmp_path):
    image_path = tmp_path / "meal.png"
    Image.new("RGBA", (2, 2), color=(255, 0, 0, 255)).save(image_path)

    script.convert_and_delete(str(tmp_path), quality=75)

    assert not image_path.exists()
    assert (tmp_path / "meal.webp").exists()


def test_convert_and_delete_skips_wellness_icon_and_non_images(tmp_path):
    wellness_dir = tmp_path / "wellness"
    wellness_dir.mkdir()
    wellness_image = wellness_dir / "photo.jpg"
    icon_image = tmp_path / "icon-marker.jpg"
    text_file = tmp_path / "notes.txt"
    Image.new("RGB", (2, 2), color="blue").save(wellness_image)
    Image.new("RGB", (2, 2), color="green").save(icon_image)
    text_file.write_text("not an image")

    script.convert_and_delete(str(tmp_path), quality=80)

    assert wellness_image.exists()
    assert icon_image.exists()
    assert text_file.exists()
    assert not (wellness_dir / "photo.webp").exists()
    assert not (tmp_path / "icon-marker.webp").exists()


def test_convert_and_delete_logs_processing_failures(tmp_path, capsys):
    bad_image = tmp_path / "broken.jpg"
    bad_image.write_text("not really an image")

    script.convert_and_delete(str(tmp_path), quality=80)

    assert bad_image.exists()
    assert "Failed to process broken.jpg" in capsys.readouterr().out


def test_main_aborts_when_user_declines(capsys):
    with patch("src.scripts.convert_images_to_webp.argparse.ArgumentParser.parse_args") as parse_args, \
         patch("builtins.input", return_value="n"), \
         patch("src.scripts.convert_images_to_webp.convert_and_delete") as convert:
        parse_args.return_value.path = "images"
        parse_args.return_value.quality = 90

        script.main()

    convert.assert_not_called()
    assert "Aborted." in capsys.readouterr().out


def test_main_converts_when_user_confirms(capsys):
    with patch("src.scripts.convert_images_to_webp.argparse.ArgumentParser.parse_args") as parse_args, \
         patch("builtins.input", return_value="Y"), \
         patch("src.scripts.convert_images_to_webp.convert_and_delete") as convert:
        parse_args.return_value.path = "images"
        parse_args.return_value.quality = 65

        script.main()

    convert.assert_called_once_with("images", 65)
    assert "Finished." in capsys.readouterr().out
