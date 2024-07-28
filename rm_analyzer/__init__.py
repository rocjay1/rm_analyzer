"""Initialize rm_analyzer."""

# Standard library imports
from importlib import resources
import os
import json

# Load the OAuth2 credentials.json file
CREDS = json.loads(
    resources.files("rm_analyzer")
    .joinpath("credentials.json")
    .read_text(encoding="UTF-8")
)

# Make sure the config file has been created
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".rma")
_config = os.path.join(CONFIG_DIR, "config.json")
if not os.path.exists(_config):
    print(f"Config file does not exist: {_config}")
    raise FileExistsError(_config)
with open(_config, encoding="UTF-8") as f:
    CONFIG = json.load(f)
