import os

from cx_Freeze import setup, Executable
import pytest
import hathi_validate
import platform

# def create_msi_tablename(python_name, fullname):
#     shortname = python_name[:6].replace("_", "").upper()
#     longname = fullname
#     return "{}|{}".format(shortname, longname)
#
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
MSVC = os.path.join(PYTHON_INSTALL_DIR, 'vcruntime140.dll')

INCLUDE_FILES = [
                    # "documentation.url",
                    #     TODO: BUILD DOCUMENTATION
                ] + pytest.freeze_includes()

# directory_table = [
#     (
#         "ProgramMenuFolder",  # Directory
#         "TARGETDIR",  # Directory_parent
#         "PMenu|Programs",  # DefaultDir
#     ),
#     (
#         "PMenu",  # Directory
#         "ProgramMenuFolder",  # Directory_parent
#         create_msi_tablename(hathi_validate.__title__, hathi_validate.FULL_TITLE)
#     ),
# ]
# shortcut_table = [
#     (
#         "startmenuShortcutDoc",  # Shortcut
#         "PMenu",  # Directory_
#         "{} Documentation".format(create_msi_tablename(hathi_validate.__title__, hathi_validate.FULL_TITLE)),
#         "TARGETDIR",  # Component_
#         "[TARGETDIR]documentation.url",  # Target
#         None,  # Arguments
#         None,  # Description
#         None,  # Hotkey
#         None,  # Icon
#         None,  # IconIndex
#         None,  # ShowCmd
#         'TARGETDIR'  # WkDir
#     ),
#     #TODO: turn back on when documentation exists
# ]

if os.path.exists(MSVC):
    INCLUDE_FILES.append(MSVC)

target_name = "hathivalidate.exe" if platform.system() == "Windows" else "hathivalidate"
setup(
    name=hathi_validate.FULL_TITLE,
    description=hathi_validate.__description__,
    version=hathi_validate.__version__,
    author=hathi_validate.__author__,
    author_email=hathi_validate.__author_email__,
    packages=[
        "hathi_validate",
        "tests"
    ],
    options={
        "build_exe": {
            "includes": ["queue", "atexit", "six", "appdirs"] + pytest.freeze_includes(),
            "include_msvcr": True,
            "packages": ["os", "lxml", "packaging"],
            "excludes": ["tkinter"],
        },
        # "bdist_msi": {
        #     "data": {
        #         "Shortcut": shortcut_table,
        #         "Directory": directory_table
        #     }
        # }
    },
    executables=[Executable("hathi_validate/cli.py",
                            targetName=target_name)],

)
