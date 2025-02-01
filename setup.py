# -*- coding: utf-8 -*-
"""Setup file for pip package creation and installation"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = list(map(str.strip, fh.readlines()))

with open("dev.requirements.txt", "r", encoding="utf-8") as fh:
    requirements_dev = list(map(str.strip, fh.readlines()))

__version__ = "0.1.1"

setuptools.setup(
    # Note: Please change the following fields to your own information
    name="demolib",
    version=__version__,
    author="John",
    author_email="linjunzhongtju@gmail.com",
    description="Utils repo template",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/JunzhongLin/internal_python_lib_gcp",
    packages=setuptools.find_packages(include=["demolib", "demolib.*"]),
    package_data={"demolib": ["../*.txt"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
)
