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
def test_chatgpt_initialization():
    """Test that ChatGPT can be initialized without errors"""
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI
    
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    # Test that ChatOpenAI can be instantiated
    try:
        chat = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)
        assert chat is not None
        assert chat.model_name == "gpt-3.5-turbo"
        assert chat.temperature == 0
    except Exception as e:
        pytest.fail(f"Failed to initialize ChatOpenAI: {e}")