from setuptools import setup, find_packages

setup(
    name="amiga_rtk",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "pyserial",
        "pyproj",
        "farm-ng-amiga"
    ],
    entry_points={
        "console_scripts": [
            "amiga_rtk = amiga_rtk.main:main"
        ]
    }
)
