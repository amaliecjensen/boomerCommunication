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


@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
def test_dotenv_loading():
    """Test that dotenv loading works without errors"""
    from dotenv import load_dotenv
    # Mock environment så vi ikke er afhængige af .env fil
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    assert api_key == 'test_key'


def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    assert 1 + 1 == 2