import yaml
from pathlib import Path


class Settings:
    def __init__(self, root_dir: Path):
        with open(Path("settings.yaml"), "r") as stream:
            try:
                data = yaml.safe_load(stream)
                self.AWS = data['AWS']
                self.SETTINGS = data['SERVER']

            except yaml.YAMLError as exc:
                print(exc)
