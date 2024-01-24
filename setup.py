"""  Created on 24/01/2024::
------------- setup.py -------------

**Authors**: L. Mingarelli
"""

import setuptools
import haver

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requirements = f.read().splitlines()


setuptools.setup(
    name="haver",
    version=haver.__version__,
    author=haver.__author__,
    author_email=haver.__email__,
    description=haver.__about__,
    url=haver.__url__,
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['haver', 'haver.tests', 'haver.res'],
    package_data={'':  ['../haver/res/*']},
    install_requires=install_requirements,
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"],
    python_requires='>=3.6',
)
