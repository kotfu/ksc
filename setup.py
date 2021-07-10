#
# -*- coding: utf-8 -*-
"""setuptools based setup for tomcatmanager

"""

from os import path

from setuptools import setup, find_packages

#
# get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ksc",
    use_scm_version=True,
    description="A command line tool and python library for documenting keyboard shortcuts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jared Crapo",
    author_email="jared@kotfu.net",
    url="https://github.com/kotfu/ksc",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="keyboard shortcut command line",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # for PEP 561
    package_data={"tomcatmanager": ["py.typed"]},
    include_package_data=True,
    #
    python_requires=">=3.6",
    install_requires=[
        "importlib_metadata>=1.6.0;python_version<'3.8'",
    ],
    setup_requires=["setuptools_scm"],
    # dependencies for development and documentation
    # $ pip install -e .[dev]
    extras_require={
        "dev": [
            "pytest",
            "pytest-mock",
            "codecov",
            "pytest-cov",
            "pylint",
            "black",
            "setuptools_scm",
            "wheel",
            "twine",
            "rope",
            "invoke",
            "sphinx",
            "sphinx-autobuild",
            "sphinx_rtd_theme",
            "autodocsumm",
            "doc8",
        ],
        "docs": [
            "sphinx",
            "sphinx-autobuild",
            "sphinx_rtd_theme",
            "autodocsumm",
            "doc8",
        ],
    },
    # define the scripts that should be created on installation
    entry_points={
        "console_scripts": [
            "ksc=ksc.__main__:main",
        ],
    },
)
