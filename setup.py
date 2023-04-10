import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yomu",
    version="0.2.0",
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="Generates the README for the 'How to Python Code' repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/how-to-python-readme",
    packages=setuptools.find_packages(),
    install_requires=[
        "feedparser>=6",
        "beautifulsoup4>=4",
        "SnakeMD>=2"
    ],
    entry_points={
        "console_scripts": [
            'yomu = yomu.readme:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License"
    ),
)
