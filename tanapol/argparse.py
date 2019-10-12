import json
import os

import yaml
import configargparse

import tanapol


config_path = os.path.join(tanapol.ROOT_DIR, 'config.yml')
p = configargparse.ArgParser(default_config_files=[config_path])
p.add('-c', '--config', required=False, is_config_file=True,
      help='custom config file path')
p.add('-v', action='count', default=0,
      help='verbosity')
p.add('--secrets-file', '-f',
      help='location of the secrets file')
p.add('--user-id',
      help='Slack user ID that is given by the slack api')
args = p.parse_args()

if args.secrets_file is None:
    secrets_path = os.path.join(tanapol.ROOT_DIR, 'secrets.yml')
else:
    secrets_path = args.secrets_file

with open(secrets_path, 'r') as secrets_file:
    secrets = yaml.safe_load(secrets_file)

db = {}
if os.path.isfile(tanapol.DB_PATH):
    with open(tanapol.DB_PATH, 'r') as db_file:
        db = json.load(db_file)
