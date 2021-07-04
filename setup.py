import setuptools

import archivebox.main

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anchorage",
    version="0.0.0",
    author="Antonio Lopez Rivera",
    author_email="antonlopezr99@gmail.com",
    description="Library to anchor your little piece of internet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonlopezr/anchorage",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "rapidjson",
        "toml",
        "archivebox==0.5.4",
        "Python-Alexandria"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)