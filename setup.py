from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="research-paper-analyzer",
    version="1.0.0",
    author="Fight1223",
    description="AI-powered research paper structure analyzer for IEEE templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.25.0",
        "PyPDF2>=4.0.0",
        "python-docx>=0.8.11",
        "markdown>=3.5.0",
        "pydantic>=2.0.0",
    ],
)
