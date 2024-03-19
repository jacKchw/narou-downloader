from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Narou novel downloader"
LONG_DESCRIPTION = "use this package to download "

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="narou_downloader",
    version=VERSION,
    author="Jack",
    author_email="jackchw.uk@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["beautifulsoup4", "requests"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=["python", "narou"],
)
