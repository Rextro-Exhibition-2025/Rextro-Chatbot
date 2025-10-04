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
            self._db_name = self._get_required_env('DB_NAME')

            self._google_client_id = self._get_required_env('GOOGLE_CLIENT_ID')    
            self._google_client_secret = self._get_required_env('GOOGLE_CLIENT_SECRET')       
            self._redirect_uri = self._get_required_env('REDIRECT_URI')
            self._redirect_frontend_uri = self.get_env_var('REDIRECT_FRONTEND_URI')


            self._db_connection_string = self._get_required_env('CONNECTION_STRING')
            self._db_name = self._get_required_env('DB_NAME')
            self._db_table_name = self._get_required_env('DB_TABLE_NAME')

            
            

            Config._initialized = True

    def _get_required_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Environment variable '{key}' is required but not set.")
        return value

    
    @property
    def openai_api_key(self) -> str:
        return self._openai_api_key

    @property
    def db_name(self) -> str:
        return self._db_name

    @property
    def google_client_id(self) -> str:
        return self._google_client_id
    
    @property
    def google_client_secret(self) -> str:
        return self._google_client_secret

    @property
    def redirect_uri(self) -> str:
        return self._redirect_uri

    @property
    def redirect_frontend_uri(self) -> str:
        return self._redirect_frontend_uri

    @property
    def db_connection_string(self) -> str:
        return self._db_connection_string

    @property
    def db_table_name(self) -> str:
        return self._db_table_name
    
    @property
    def db_name(self) -> str:
        return self._db_name
    
   

   

    

    # General getter for any env variable
    def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.getenv(key, default)

    # Hide secrets in debug output
    def __repr__(self) -> str:
        return f"<Config(openai_api_key={'*' * 10 if self._openai_api_key else None}, google_client_id={'*' * 10 if self._google_client_id else None})>"

# Singleton accessor
def get_config() -> Config:
    return Config()
