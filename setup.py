from setuptools import find_packages, setup

# Read README for the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def __version__():
    return "0.1.0b11"  # Incremented version number


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
        "torch",
        "gguf",
        "uvicorn[standard]",
        "requests==2.32.3",
        "spacy==3.7.5",
        "pydantic>=2.8.2,<3.0.0",
        "sentencepiece",
        "protobuf",
        "aiohttp",
        "numpy",
        "fastapi",
        "asyncio",
        "setuptools",
        "pydantic-settings==2.3.4",
        "typer==0.12.3",
        "sqlmodel",
        "sphinx",
        "cryptography",
        "rellm",
        "transformers",
        "sentence-transformers",
        "python-dotenv",
        "regex",
        "uuid",
        "rich",
    ],
    extras_require={
        "dev": [
            "just",
            "isort",
            "black",
            "blacken-docs",
            "certifi",
            "flake8",
            "prettier",
            "tox",
            "pytest==7.4.0",
            "pytest-asyncio==0.21.0",
            "pytest-cov",
            "mypy",
            "autoflake",
            "pre-commit",
        ],
    },
    python_requires=">=3.10,<3.13",
    entry_points={
        "console_scripts": [
            "datafog-instructor=app.main:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: tox",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
    ],
    keywords="transformers, models, language, models, embeddings, sentence-transformers, rag, huggingface, hugging-face, hugging-face-transformers, huggingface-transformers, huggingface-models, huggingface-embeddings, huggingface-sentence-transformers",
    maintainer="Sid Mohan (DataFog, Inc.)",
    maintainer_email="sid@datafog.ai",
    url="https://datafog.ai",
    project_urls=project_urls,
    license="MIT",
)
