import unittest
from io import StringIO
from unittest.mock import patch

from package_statistics import (parse_debian_contents_file,
                                summarize_package_statistics)


class TestPackageStatistics(unittest.TestCase):
    def setUp(self) -> None:
        self.package_statistics = {
            "package1": 10,
            "package2": 5,
            "package3": 15,
            "package4": 20,
            "package5": 1
        }

    def test_parse_debian_contents_file(self):
        input_content = """
            usr/share/screen/utf8encodings/c6          debian-installer/screen-udeb
            usr/share/screen/utf8encodings/c7          debian-installer/screen-udeb
            usr/share/screen/utf8encodings/c8          debian-installer/screen-udeb
            usr/share/screen/utf8encodings/cc          debian-installer/screen-udeb
            usr/share/screen/utf8encodings/cd          debian-installer/screen-udeb
            usr/share/screen/utf8encodings/d6          debian-installer/screen-udeb
            usr/share/terminfo/b/bterm                 debian-installer/bogl-bterm-udeb,debian-installer/rootskel-gtk
            usr/share/themes/Clearlooks/gtk-2.0/gtkrc  debian-installer/rootskel-gtk
            usr/share/themes/dark/gtk-2.0/gtkrc        debian-installer/rootskel-gtk
            usr/share/themes/dark/gtk-2.0/gtkrc 92     debian-installer/rootskel-gtk
        """
        expected_output = {
            "debian-installer/screen-udeb": 6, 
            "debian-installer/bogl-bterm-udeb": 1,
            "debian-installer/rootskel-gtk": 3
        }
        actual_output = parse_debian_contents_file(input_content)

        self.assertDictEqual(actual_output, expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_summarize_package_statistics(self, mock_stdout) -> None:
        expected_output = [
            "Displaying all 5 packages.",
            "package name      number of files",
            "package4          20",
            "package3          15",
            "package1          10",
            "package2          5",
            "package5          1",
        ]
        summarize_package_statistics(self.package_statistics)

        self.assertEqual(mock_stdout.getvalue().strip().split("\n"), expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_summarize_package_statistics_with_lower_top_n(self, mock_stdout) -> None:
        expected_output = [
            "package name      number of files",
            "package4          20",
            "package3          15",
        ]
        summarize_package_statistics(self.package_statistics, top_n=2)

        self.assertEqual(mock_stdout.getvalue().strip().split("\n"), expected_output)

    def test_summarize_package_statistics_with_negative_top_n(self) -> None:
        with self.assertRaises(ValueError):
            summarize_package_statistics(self.package_statistics, top_n=-2)
