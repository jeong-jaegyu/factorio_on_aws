import os
from pathlib import Path

import boto3
from local_modules import persistance_parser
from local_modules import settings_parser
# init pparser
p = persistance_parser.PParser(Path('.'))

# init sparser
s = settings_parser.Settings(Path('.'))


if __name__ == '__main__':
    bucket_UUID = p.search_byname('factorio')['uuid']
    object_name = s.SETTINGS['world']

    s3 = boto3.client('s3',
                      aws_access_key_id=s.AWS['aws_access_key_id'],
                      aws_secret_access_key=s.AWS['aws_secret_access_key'])

    os.makedirs(Path('./resources/in'), exist_ok=True)
    with open(Path('./resources/in/', 'Hrmmm.zip'), 'wb') as f:
        s3.download_fileobj(bucket_UUID, object_name, f)
