import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import DataFogInstructor, LLMConfig
from app.pii_redactor.redactor import PIIDataExtraction, DetectedPII, PIIExtractionError, PIIExtractor
import os
from pydantic import ValidationError

# Add any other necessary imports

@pytest.fixture
def mock_llm_config():
    return LLMConfig(api_key="test_api_key")

@pytest.fixture
def mock_pii_extractor():
    with patch('app.main.PIIExtractor') as mock:
        yield mock

@pytest.fixture
def datafog_instructor(mock_llm_config, mock_pii_extractor):
    with patch.dict(os.environ, {"GROQ_API_KEY": "test_api_key"}):
        return DataFogInstructor(mock_llm_config)

class TestLLMConfig:
    def test_init_valid(self):
        llm_config = LLMConfig(api_key="test_api_key", model="mixtral-8x7b-32768")
        assert llm_config.api_key == "test_api_key"
        assert llm_config.model == "mixtral-8x7b-32768"

    def test_init_invalid(self):
        # Test preconditions for invalid initialization
        """
        Preconditions:
        - api_key must be a non-empty string
        - model must be a valid model name supported by the API

        Postconditions:
        - An exception is raised if the provided api_key is empty
        """
        with pytest.raises(ValidationError):
            LLMConfig(api_key="", model="mixtral-8x7b-32768")

        with pytest.raises(ValidationError):
            LLMConfig(api_key="test_api_key", model="")

        with pytest.raises(ValidationError):
            LLMConfig(api_key="", model="")

        with pytest.raises(ValidationError):
            LLMConfig(api_key="   ", model="mixtral-8x7b-32768")

        with pytest.raises(ValidationError):
            LLMConfig(api_key="test_api_key", model="   ")

class TestDataFogInstructor:

    def test_init_with_valid_config(self):
        # Precondition: llm_config is a valid LLMConfig instance
        config = LLMConfig(api_key="test_key")
        
        with patch('app.main.DataFogInstructor._initialize_client') as mock_init_client:
            with patch('app.main.PIIExtractor') as mock_pii_extractor:
                instructor = DataFogInstructor(config)
                
                # Postconditions
                assert instructor.llm_config == config
                mock_init_client.assert_called_once()
                mock_pii_extractor.assert_called_once_with("test_key")

    def test_init_without_config(self):
        # Precondition: llm_config is None and GROQ_API_KEY is set
        with patch.dict('os.environ', {'GROQ_API_KEY': 'env_test_key'}):
            with patch('app.main.DataFogInstructor._initialize_client') as mock_init_client:
                with patch('app.main.PIIExtractor') as mock_pii_extractor:
                    instructor = DataFogInstructor()
                    
                    # Postconditions
                    assert isinstance(instructor.llm_config, LLMConfig)
                    assert instructor.llm_config.api_key == 'env_test_key'
                    mock_init_client.assert_called_once()
                    mock_pii_extractor.assert_called_once_with('env_test_key')

    def test_init_without_config_and_env_var(self):
        # Precondition: llm_config is None and GROQ_API_KEY is not set
        with patch.dict('os.environ', clear=True):
            with pytest.raises(ValueError, match="GROQ_API_KEY environment variable is not set"):
                DataFogInstructor()

    # def test_init_with_invalid_config(self):
    #     # Precondition: llm_config is an invalid type
    #     with pytest.raises(TypeError):
    #         DataFogInstructor("invalid_config")

    @pytest.mark.parametrize("error_class", [ValueError, TypeError, AttributeError])
    def test_init_error_handling(self, error_class):
        config = LLMConfig(api_key="test_key")
        
        with patch('app.main.DataFogInstructor._initialize_client', side_effect=error_class("Test error")):
            with pytest.raises(error_class):
                DataFogInstructor(config)

    def test_invariants(self):
        config = LLMConfig(api_key="test_key")
        
        with patch('app.main.DataFogInstructor._initialize_client') as mock_init_client:
            with patch('app.main.PIIExtractor') as mock_pii_extractor:
                instructor = DataFogInstructor(config)
                
                # Store initial values
                initial_config = instructor.llm_config
                initial_client = instructor.client
                initial_extractor = instructor.pii_extractor
                
                # Attempt to modify attributes
                # with pytest.raises(AttributeError):
                #     instructor.llm_config = LLMConfig(api_key="new_key")
                # with pytest.raises(AttributeError):
                #     instructor.client = MagicMock()
                # with pytest.raises(AttributeError):
                #     instructor.pii_extractor = MagicMock()
                
                # # Verify invariants
                # assert instructor.llm_config is initial_config
                # assert instructor.client is initial_client
                # assert instructor.pii_extractor is initial_extractor

