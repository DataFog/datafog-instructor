# DataFog Instructor

## Demo

datafog-instructor lets you use open-source LLMs (HF models, models ending in .gguf) and instruct them to return only specific, user-defined outputs like entity tags, JSON-only structured output, and synthetic data templates, among others.  
We do this by using advanced ML methods that constrain the set of tokens a model will generate next when it's providing a response, and this allows us to achieve a far higher rate of accuracy and precision than baseline LLM output methods (for more, see the evals.ipynb file in examples).

## Installation

```
pip install --upgrade datafog-instructor
```

## Quick Start

To see a list of all available options, you can type

```
datafog-instructor --help
```

Which should show you a screen like this:
![Help Menu](public/help-menu.png)

### Initialize

Begin by entering the following into your terminal post-install:

```
datafog-instructor init
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
