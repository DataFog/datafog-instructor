# DataFog Instructor

v0.1.0 Release Notes

Hi folks, based on some feedback a few important changes:

- We have shifted away from the CLI approach to a more flexible API-based solution. For v0.1.0, you'll need to clone the repository and install dependencies using Poetry.
- The env.example file now includes a LOGFIRE_TOKEN. You can obtain one by signing up at https://logfire.pydantic.dev. Logfire is an observability platform developed by the Pydantic team, designed to assist with debugging and monitoring, including LLM calls.
- This version focuses on producing consistent LLM outputs for PII detection and incorporates extensive error handling to create a more production-ready service.
- We've implemented robust validation and error handling throughout the codebase to ensure reliability and ease of debugging.

Start by cloning the repo and installing the dependencies using poetry:

```
git clone https://github.com/datafog/datafog-instructor.git
cd datafog-instructor
poetry install
```

You'll also need to create a `.env` file with the OPENAI_API_KEY and GROQ_API_KEY.  You can get these by signing up for accounts at https://openai.com/ and https://www.groq.com/.

Once you have the .env file, you can run the following to start the service:

```
uvicorn app.main:app --reload
```


## Sample CURL Commands


```
curl -X POST "http://localhost:8000/extract-pii" \     
     -H "Content-Type: application/json" \
     -d '{"content": "My name is John Doe and my email is john.doe@example.com. My phone number is 123-456-7890."}'
```

a default config file containing information about the model, tokenizer, regex_pattern gets loaded into your working directory.

You can see the contents of that file by typing:

```
datafog-instructor show-fogprint
```

What is a fogprint? A fogprint is a template that you can re-use, with specific configuration settings for the models, filenames, model_ids, and other important information to instruct an LLM to detect entities. This file is currently saved as fogprint.json.

### Verify the installation:

```

datafog-instructor list-entities

```

You should see a list of default entity types: PERSON, COMPANY, LOCATION, and ORG.

## Sample Operations

### Detect Entities in Text

```

datafog-instructor detect-entities --prompt "Apple Inc. was founded by Steve Jobs in Cupertino, California."

```

This will output a table of detected entities, their positions, and types.

### Display Current Configuration

```

datafog-instructor show-fogprint

```

This command will show you the current configuration stored in `fogprint.json`.

### Reinitialize with Custom Settings

To change the default model or pattern:

1. Edit the `fogprint.json` file directly, or
2. Use the `init` command with the `--force` flag:

```

datafog-instructor init --force

```

Follow the prompts to update your configuration.

## Advanced Usage

- Adjust the maximum number of tokens generated:

```

datafog-instructor detect-entities --prompt "Your text here" --max-new-tokens 100

```

- For batch processing or integration into your Python projects, import the `EntityDetector` class from `models.py`.

## Development and Testing

For development purposes, you can install additional dependencies:

```

python -m venv venv && source venv/bin/activate && pip install requirements-dev.txt

## Documentation

To build the documentation locally:

```

pip install datafog-instructor[docs]
cd docs
sphinx

```

The documentation will be available in the `docs/_build/html` directory.

## Contributing

Contributions to the DataFog Instructor SDK are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository or join our Discord community at https://discord.gg/bzDth394R4.

## Links

- Homepage: https://datafog.ai
- Documentation: https://docs.datafog.ai
- Twitter: https://twitter.com/datafoginc
- GitHub: https://github.com/datafog/datafog-instructor
```
