import yaml

def load(config_file='config.yml'):
  """Loads the provided yaml config file."""
  try:
    config = _load_config(os.path.abspath(config_file))
  except:
    raise SystemExit('Failed to load configuration file, {}. Review your config and try again.'.format(config_file))
  return config

def _load_config(config_file):
  with open(config_file, "r", encoding="utf8") as config:
    return yaml.safe_load(config)