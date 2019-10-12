import os

import tanapol
import configargparse


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
