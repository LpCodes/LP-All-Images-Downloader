from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Project summary
summary = "A Python package to automate image downloading from a given URL."

# Keywords
keywords = ['image', 'download', 'automation', 'web scraping', 'selenium', 'webdriver_manager']

# License
license = "MIT License"

# Author email
author_email = "lovelesh_p@zohomail.in"

# Minimum Python version required
python_requires = ">=3.6"

setup(
    name="LpImagesDownloader",
    version="0.0.9",
    author="Lpcodes",
    author_email=author_email,
    description=summary,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/LpCodes/LP-All-Images-Downloader",
    project_urls={
        "Bug Tracker": "https://github.com/LpCodes/LP-All-Images-Downloader/issues",
        "Source Code": "https://github.com/LpCodes/LP-All-Images-Downloader",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    keywords=keywords,
    install_requires=[
        'requests',
        'validators',
        'selenium',
        'webdriver_manager',
    ],
    python_requires=python_requires,
)
