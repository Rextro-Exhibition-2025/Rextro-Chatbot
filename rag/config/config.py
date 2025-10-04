import os
from typing import Optional
import tempfile, json
from dotenv import load_dotenv

class Config:
    _instance: Optional['Config'] = None
    _initialized: bool = False

    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            
            if os.path.isfile('.env'):
                load_dotenv()

            
            self._openai_api_key = self._get_required_env('OPENAI_API_KEY')
            

            
            

            Config._initialized = True

    def _get_required_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Environment variable '{key}' is required but not set.")
        return value

    
    @property
    def openai_api_key(self) -> str:
        return self._openai_api_key

   
    
   

   

    

    # General getter for any env variable
    def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.getenv(key, default)

    # Hide secrets in debug output
    def __repr__(self) -> str:
        return f"<Config(openai_api_key={'*' * 10 if self._openai_api_key else None}, google_client_id={'*' * 10 if self._google_client_id else None})>"

# Singleton accessor
def get_config() -> Config:
    return Config()
