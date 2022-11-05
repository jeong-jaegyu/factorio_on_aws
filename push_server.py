import logging
from datetime import date

import boto3
from botocore.exceptions import ClientError
import os
from pathlib import Path
from local_modules import persistance_parser
from local_modules import settings_parser

# P init
p = persistance_parser.PParser(Path('.').absolute())

# settings init
s = settings_parser.Settings(Path('.').absolute())

## logger init (date)
os.makedirs(Path('./logs'), exist_ok=True)
logfile = f'logs/{date.today()}'
logging.basicConfig(filename=logfile,
                    format='[%(asctime)s] %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    encoding='utf-8',
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    global response
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',
                             aws_access_key_id=s.AWS['aws_access_key_id'],
                             aws_secret_access_key=s.AWS['aws_secret_access_key'])

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False, response
    return True, response


# Driver code
if __name__ == '__main__':
    import sys
    os.makedirs(Path('./resources/out'), exist_ok=True)
    if len(sys.argv) > 2:
        success_status, response = upload_file(file_name=str(Path(sys.argv[1]).absolute()),
                                               bucket=p.search_byname('factorio')['uuid'],
                                               object_name=sys.argv[2] if (len(sys.argv) > 2) else None)
        if success_status:
            logger.info(f"World Upload Succeeded.")
        else:
            logger.critical(f"!!-- World Upload Failed with response: {response} --!!")

    else:
        success_status, response = upload_file(str(Path("./resources/out/", )),
                                               bucket=p.search_byname('factorio')['uuid'],
                                               object_name=s.SETTINGS['world'])
        if success_status:
            logger.info(f"World Upload Succeeded.")
        else:
            logger.critical(f"!!-- World Upload Failed with response: {response} --!!")
