from setuptools import setup, find_packages
import configparser
config = configparser.ConfigParser(allow_no_value=True)
config.read('database.ini')


# Setting up
setup(
    version="1.0.4",
    name=str(config["current"]["name"]), 
    author="",
    author_email="",
    packages=find_packages(),
)