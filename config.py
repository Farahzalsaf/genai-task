import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

print("Sections:", config.sections())
for section in config.sections():
    print(section, dict(config.items(section)))

# Database Configuration
DB_HOST = config['database']['host']
DB_PORT = config['database'].getint('port')
DB_USERNAME = config['database']['username']
DB_PASSWORD = config['database']['password']
DB_DATABASE = config['database']['database']
# Server Configuration
SERVER_HOST = config['server']['host']
SERVER_PORT = config['server'].getint('port')
# OpenAI Configuration
OPENAI_API_KEY = config['openai']['api_key']
Ollama = config['ollama']['api_key']
# JWT Configuration
#SECRET_KEY = config['secret']['secret_key']

# # Uncomment if you have these sections
# # Logging Configuration
# # LOGGING_CONFIG = config['logging']['config']

# # Email Configuration
# # EMAIL_HOST = config['email']['host']
# # EMAIL_PORT = config['email'].getint('port')
