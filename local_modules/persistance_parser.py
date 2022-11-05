import json as j
import os
from datetime import date
import logging
from pathlib import Path


class PParser:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        with open('buckets.json') as bucket_file:
            self.bucket_json = j.load(bucket_file)
            self.names = [item['name'] for item in self.bucket_json['buckets']]
            self.uuids = [item['uuid'] for item in self.bucket_json['buckets']]

    def buckets(self):
        return self.bucket_json['buckets']

    def store(self, name, uuid):
        try:
            self.bucket_json['buckets'].append({"name": name, "uuid": uuid})
            with open(Path.joinpath(self.root_dir, 'buckets.json'), 'w') as f:
                j.dump(self.bucket_json, f, indent=4)
        except Exception as e:
            logger.critical("!!-- Could not write to file. Aborting. --!!")
            raise e

    def search_byname(self, name):
        for item in self.bucket_json['buckets']:
            if item['name'] == name:
                return item

    def search_byuuid(self, uuid):
        for item in self.bucket_json['buckets']:
            if item['uuid'] == uuid:
                return item


# logger stuff
os.makedirs(Path('./logs'), exist_ok=True)
logfile = f'logs/{date.today()}'
logging.basicConfig(filename=logfile,
                    format='[%(asctime)s] %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    encoding='utf-8',
                    datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)
# \ logger stuff

