from __future__ import absolute_import

VERSION = (0, 9, 1)
__version__ = '.'.join(map(str, VERSION))

import sys
import os
# print sys.path
sys.path.insert(0,r"{0}/celery_distribute_crawler".format(os.getcwd()))
# sys.path.insert(0,"~/dis/celery_distribute_crawler/flower/")
# print sys.path
import os
# print os.getcwd()