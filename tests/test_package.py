import os

import pytest
from hathi_validate import package


class mockDirEntry:
    def __init__(self, name, source, is_dir):
        self.name = name
        self.path = os.path.join(source, name)
        self._is_dir = is_dir

    def is_dir(self):
        return self._is_dir


@pytest.fixture()
def sample_hathi_package(monkeypatch):
    def mockreturn(path):
        return [
            mockDirEntry(name="00000001.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000001.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000002.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000002.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000003.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000003.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000004.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000004.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000005.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000005.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000006.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000006.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000007.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000007.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000008.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000008.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000009.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000009.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000010.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000010.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000011.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000011.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000012.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000012.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000013.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000013.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000014.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000014.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000015.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000015.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000016.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000016.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000017.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000017.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000018.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000018.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000019.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000019.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000020.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000020.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000021.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000021.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000022.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000022.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000023.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000023.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000024.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000024.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000025.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000025.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000026.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000026.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000027.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000027.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000028.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000028.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000029.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000029.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000030.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000030.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000031.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000031.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000032.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000032.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000033.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000033.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000034.jp2", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="00000034.txt", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="checksum.md5", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="marc.xml", source="c:\\my_hathi_package\\721932", is_dir=False),
            mockDirEntry(name="meta.yml", source="c:\\my_hathi_package\\721932", is_dir=False),
        ]

    monkeypatch.setattr(os, "scandir", mockreturn)


@pytest.fixture()
def sample_hathi_package_folder(monkeypatch):
    def mockreturn(path):
        return [
            mockDirEntry(name="2693684", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="2942435", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="6852190", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="7213538", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="7213857", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="7213932", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="7214043", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="7215655", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="7215682", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="7215700", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="7465982", source="c:\\my_hathi_package", is_dir=True),
            mockDirEntry(name="8102529", source="c:\\my_hathi_package", is_dir=True),

            ]


    monkeypatch.setattr(os, "scandir", mockreturn)


def test_get_folders(sample_hathi_package_folder):
    expected_paths =[
        "c:\\my_hathi_package\\2693684",
        "c:\\my_hathi_package\\2942435",
        "c:\\my_hathi_package\\6852190",
        "c:\\my_hathi_package\\7213538",
        "c:\\my_hathi_package\\7213857",
        "c:\\my_hathi_package\\7213932",
        "c:\\my_hathi_package\\7214043",
        "c:\\my_hathi_package\\7215655",
        "c:\\my_hathi_package\\7215682",
        "c:\\my_hathi_package\\7215700",
        "c:\\my_hathi_package\\7465982",
        "c:\\my_hathi_package\\8102529",
    ]

    for x in package.get_dirs("c:\\my_hathi_package"):
        assert x in expected_paths
