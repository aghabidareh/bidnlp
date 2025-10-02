from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bidnlp",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Persian (Farsi) Natural Language Processing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bidnlp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Persian",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Add your dependencies here
    ],
)
