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
    # Dette burde ikke give exceptions
    load_dotenv()
    assert True


@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
def test_openai_key_retrieval():
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY") #tester at vi kan få fat i vores openapi
    assert api_key == 'test_key'


