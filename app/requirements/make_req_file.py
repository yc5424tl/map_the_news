import logging
import os
import sys

logger = logging.getLogger(__name__)

DEPLOYMENT = os.environ.get("DEPLOYMENT")

try:

    with open(os.path.join(sys.path[0], 'common.txt'), 'r') as common, open(os.path.join(sys.path[0], 'requirements.txt'), 'w') as reqs:
        com_reqs = common.readlines()
        reqs.writelines(com_reqs)
        reqs.write('\n')

        if DEPLOYMENT == "DEV":
            with open(os.path.join(sys.path[0], 'dev.txt'), 'r') as dev:
                dev_reqs = dev.readlines()
                reqs.writelines(dev_reqs)

        elif DEPLOYMENT == "PROD":
            with open(os.path.join(sys.path[0], 'prod.txt'), 'r') as prod:
                prod_reqs = prod.readlines()
                reqs.writelines(prod_reqs)

except IOError as ioE:
    logger.log(lvl=logging.Error, msg=f"IOError while creating requirements.txt file: {ioE}")
    open(os.path.join(sys.path[0], 'requirements.txt'), 'a').close()
