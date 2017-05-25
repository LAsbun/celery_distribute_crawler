from __future__ import absolute_import

VERSION = (1, 0, 0)
__version__ = '.'.join(map(str, VERSION)) + '-dev'

import sys
import os
# print sys.path
sys.path.insert(0,r"{0}/celery_distribute_crawler".format(os.getcwd()))
# sys.path.insert(0,"~/dis/celery_distribute_crawler/flower/")
# print sys.path
import os
print os.getcwd()