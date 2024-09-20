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

## Contributing

Contributions to the DataFog Instructor SDK are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository or join our Discord community at https://discord.gg/bzDth394R4.

## Acknowledgements

- Logfire: https://logfire.pydantic.dev
- Pydantic: https://pydantic.dev
- Instructor: https://github.com/jxnl/instructor

## Links

- Homepage: https://datafog.ai
- Documentation: https://docs.datafog.ai
- Twitter: https://twitter.com/datafoginc
- GitHub: https://github.com/datafog/datafog-instructor
```
