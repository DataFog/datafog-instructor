from .config import config

def get_llm():
    from .core import OllamaLLM
    
    if config.llm_backend == "ollama":
        return OllamaLLM(config.llm_endpoint, config.llm_model)
    elif config.llm_backend == "openai":
        print('not supported yet')
    else:
        raise ValueError(f"Unsupported LLM backend: {config.llm_backend}")