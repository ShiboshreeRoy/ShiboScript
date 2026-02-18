"""Setup script for ShiboScript - Professional Edition"""
import os
from setuptools import setup, find_packages

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="shiboscript-pro",
    version="1.0.0",
    author="ShiboShreeRoy",
    author_email="shiboshreeroycse@gmail.com",
    description="A lightweight scripting language for education and automation - Production Ready",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShiboShreeRoy/ShiboScript",
    project_urls={
        "Bug Reports": "https://github.com/ShiboShreeRoy/ShiboScript/issues",
        "Source": "https://github.com/ShiboShreeRoy/ShiboScript",
        "Documentation": "https://shiboscript.readthedocs.io/",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Education",
        "Topic :: Utilities",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "flake8",
            "black",
            "mypy",
        ],
        "gui": [
            "customtkinter",
            "tkinter",
        ],
        "web": [
            "requests",
        ],
        "full": [
            "customtkinter",
            "requests",
            "pillow",
        ],
    },
    entry_points={
        "console_scripts": [
            "shiboscript=shiboscript.cli:main",
            "shibo=shiboscript.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "shiboscript": ["assets/*", "templates/*", "config/*"],
    },
    keywords="scripting language interpreter education automation",
    zip_safe=False,
)
