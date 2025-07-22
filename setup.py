from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="build-llm-from-scratch",
    version="0.1.0",
    author="Ali Zeeshan",
    author_email="dexterous02@gmail.com",
    description="A comprehensive implementation of Large Language Models from scratch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alizeeshan-07/Build_LLM_From_Scratch",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=22.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "flake8>=5.0.0",
            "mypy>=0.971",
        ],
    },
    entry_points={
        "console_scripts": [
            "build-llm=src.utils.cli:main",
        ],
    },
)