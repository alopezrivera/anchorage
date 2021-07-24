import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anchorage",
    version="1.0.0.0",
    author="Antonio Lopez Rivera",
    author_email="antonlopezr99@gmail.com",
    description="Anchor your little piece of internet.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonlopezr/anchorage",
    entry_points={
        "console_scripts": [
            "anchorage = anchorage.cli:main",
        ],
    },
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "rapidjson",
        "toml",
        "Python-Alexandria",
        "archivenow",
        "internetarchive",
        "tqdm",
        "pyfiglet",
        "PyInquirer",
        "prompt-toolkit==1.0.14",
        "lz4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
