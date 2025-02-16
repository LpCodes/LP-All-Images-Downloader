from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LpImagesDownloader",
    version="1.0.0",
    author="Lpcodes",
    author_email="lovelesh_p@zohomail.in",
    description="A Python package to automate image downloading from a given URL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LpCodes/LP-All-Images-Downloader",
    project_urls={
        "Bug Tracker": "https://github.com/LpCodes/LP-All-Images-Downloader/issues",
        "Source Code": "https://github.com/LpCodes/LP-All-Images-Downloader",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    keywords=['image', 'download', 'automation', 'web scraping', 'selenium', 'webdriver_manager'],
    install_requires=[
        'requests>=2.26.0',
        'validators>=0.18.2',
        'selenium>=4.0.0',
        'webdriver_manager>=3.5.0',
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'lpimagesdownloader=image_downloader:download_images',
        ],
    },
)
