from setuptools import find_packages, setup

# Read README for the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

def __version__():
    return "0.1.0b8"  # Incremented version number

project_urls = {
    "Homepage": "https://datafog.ai",
    "Documentation": "https://docs.datafog.ai",
    "Discord": "https://discord.gg/bzDth394R4",
    "Twitter": "https://twitter.com/datafoginc",
    "GitHub": "https://github.com/datafog/datafog-instructor",
}

setup(
    name="datafog-instructor",
    version=__version__(),
    author="Sid Mohan",
    author_email="sid@datafog.ai",
    description="Scan, redact, and manage PII in your documents before they get uploaded to a Retrieval Augmented Generation (RAG) system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pydantic==2.7.1",
        "ollama>=0.2.0,<0.3.0",
        "ollama-instructor==0.2.0",
        "python-dotenv==1.0.1",
        "openai==1.12.0",
        "click==8.1.7",
    ],
    extras_require={
        "dev": [
            "pytest==8.0.0",
            "black==24.1.1",
            "flake8==7.0.0",
            "mypy==1.8.0",
            "types-requests==2.31.0.20240218",
        ],
        "docs": [
            "sphinx==7.2.6",
            "sphinx-rtd-theme==2.0.0",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
    ],
    keywords="pii, redaction, nlp, rag, retrieval augmented generation, entity recognition",
    maintainer="DataFog",
    maintainer_email="hi@datafog.ai",
    url="https://datafog.ai",
    project_urls=project_urls,
    license="MIT",
)