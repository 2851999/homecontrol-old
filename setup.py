#!/bin/python
import setuptools

setuptools.setup(
    name="homecontrol",
    version="0.0.6",
    author="2851999",
    author_email="2851999@users.noreply.github.com",
    description="A library and flask API for controlling home appliances",
    license="Apache License 2.0",
    url="https://github.com/2851999",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "msmart",
        "requests-toolbelt",
        "APScheduler",
    ],
)
