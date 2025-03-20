import streamlit as st
import pandas as pd
import os
from cryptography.fernet import Fernet
import base64
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


# Encryption setup
def get_or_create_key():
    """Securely handle encryption key"""
    key_env_var = "INTERVIEW_ENCRYPTION_KEY"
    if key_env_var in os.environ:
        return os.environ[key_env_var].encode()
    
    key_file = "secret.key"
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as key_file:
            key_file.write(key)
        os.chmod(key_file, 0o400)
    with open(key_file, "rb") as f:
        return f.read()

cipher_suite = Fernet(get_or_create_key())


def decrypt_data(encrypted_data):
    """Decrypt data for authorized access only"""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()


print(decrypt_data('gAAAAABn2qO2eUP0RJ8IdbHJom7RlgrOwJY-89tU0jLl9bMXCqpwV5L0MvfUjozWpyB5QId6tg0IZKecVdiwHDHjOLYXhfE7lA=='))