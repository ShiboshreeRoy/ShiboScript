from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shiboscript",
    version="1.0.0",
    author="Shiboscript Team",
    author_email="shiboshreeroycse@gmail.com",
    description="A Python-like scripting language with advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shiboscript/shiboscript",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "shiboc=shiboscript.compiler:main",
            "shiboscript=shiboscript.core:repl",
        ],
    },
    install_requires=[
        "Pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    scripts=['shiboc'],  # Add the shiboc script
)