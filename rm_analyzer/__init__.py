"""Initialize rm_analyzer."""

# Standard library imports
from importlib import resources
import os
import json

# Load the OAuth2 credentials.json file
# PyInstaller will compile it into the executable
CREDS = json.loads(
    resources.files("rm_analyzer")
    .joinpath("credentials.json")
    .read_text(encoding="UTF-8")
)

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Create the config directory if it doesn't exist
_config_dir = os.path.join(os.path.expanduser("~"), ".rma")
if not os.path.exists(_config_dir):
    os.mkdir(_config_dir)
CONFIG_DIR = _config_dir

# Make sure the config file has been created
_config = os.path.join(_config_dir, "config.json")
if not os.path.exists(_config):
    print(f"Config file does not exist: {_config}")
    print("Create the config file before continuing.")
    raise FileNotFoundError(_config)
with open(_config, encoding="UTF-8") as f:
    CONFIG = json.load(f)
