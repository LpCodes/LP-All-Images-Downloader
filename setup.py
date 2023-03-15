from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LpImagesDownloader",
    version="0.0.8",
    author="Lpcodes",
    description="A package for downloading all the Images from the URL provided",
    long_description_content_type="text/markdown",
    long_description=long_description,
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
    keywords='Images Image download automation auto webscrapping web selenium',
    install_requires=[
        'requests',
        'validators',
        'selenium',
        'webdriver_manager',
    ],
    python_requires=">=3.6",)
