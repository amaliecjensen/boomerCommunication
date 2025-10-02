"""
Basic tests for boomerCommunication project
"""
import os
import pytest
from unittest.mock import patch


def test_environment_setup():
    """Test that basic environment setup works"""
    # Test that we can import required modules
    try:
        from dotenv import load_dotenv
        from langchain_openai import ChatOpenAI
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")


def test_dotenv_loading():
    """Test that dotenv loading works without errors"""
    from dotenv import load_dotenv
    
    # This should not raise any exceptions
    load_dotenv()
    assert True


@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
def test_openai_key_retrieval():
    """Test that OpenAI API key can be retrieved from environment"""
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    assert api_key == 'test_key'


@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
@patch('langchain_openai.ChatOpenAI')
def test_chatgpt_initialization(mock_chatgpt):
    """Test that ChatGPT can be initialized without errors"""
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI
    
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    # Mock the ChatOpenAI initialization
    mock_instance = mock_chatgpt.return_value
    mock_instance.model_name = "gpt-3.5-turbo"
    mock_instance.temperature = 0
    
    # Test that ChatOpenAI can be called with correct parameters
    chat = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)
    
    # Verify that ChatOpenAI was called with correct parameters
    mock_chatgpt.assert_called_once_with(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)
    assert chat is not None