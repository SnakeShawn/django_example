'''
Author:
Date:
Version:
Description: Capture the console output.
'''

import sys
import contextlib
from io import StringIO

@contextlib.contextmanager
def stdoutIO(stdout=None):
    oldStd = sys.stdout
    if stdout is None:
        stdout = StringIO()

    sys.stdout = stdout
    yield stdout
    sys.stdout = oldStd


