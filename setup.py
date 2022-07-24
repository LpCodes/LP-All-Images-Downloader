from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LpImagesDownloader",
    version="0.0.5",
    author="Lpcodes",
    description="A package for downloading all the Images from the URL provided",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LpCodes/LP-All-Images-Downloader",
    project_urls={
        "Bug Tracker": "https://github.com/LpCodes/LP-All-Images-Downloader/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=['requests','selenium','validators','webdriver_manager'],
    python_requires=">=3.6",)
