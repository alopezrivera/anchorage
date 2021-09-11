import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anchorage",
    version="1.2.1.0",
    author="Antonio Lopez Rivera",
    author_email="antonlopezr99@gmail.com",
    description="Python library and CLI to anchor your little piece of internet.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alopezrivera/anchorage",
    entry_points={
        "console_scripts": [
            "anchorage = anchorage.cli:main",
        ],
    },
    packages=setuptools.find_packages(),
    install_requires=[
        "setuptools",
        "numpy",
        "rapidjson",
        "toml",
        "Python-Alexandria",
        "wayback",
        "archivenow",
        "tqdm",
        "pyfiglet",
        "PyInquirer",
        "prompt-toolkit==1.0.14",
        "lz4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
