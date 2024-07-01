from setuptools import setup, find_packages

setup(
    name="datafog_instructor",
    version="0.1.0b1",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "ollama",
        "ollama_instructor",
        "python-dotenv"

    ],
    author="Sid Mohan",
    author_email="sid@datafog.ai",
    description="A brief description of datafog_instructor",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/datafog/datafog-python",
)