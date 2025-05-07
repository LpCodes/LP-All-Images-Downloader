from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LpImagesDownloader",
    version="1.1.0",
    author="Lpcodes",
    author_email="lovelesh_p@zohomail.in",
    description="A powerful Python package to automate image downloading from any webpage with robust error handling and detailed logging.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LpCodes/LP-All-Images-Downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        'requests>=2.28.2,<3.0.0',
        'selenium>=4.8.2,<5.0.0',
        'validators>=0.20.0,<0.21.0',
        'webdriver_manager>=3.8.5,<4.0.0',
    ],
    entry_points={
        'console_scripts': [
            'lpimagesdownloader=LpImagesDownloader.lid:download_images',
        ],
    },
) 