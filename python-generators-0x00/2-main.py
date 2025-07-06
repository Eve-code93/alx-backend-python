#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

# Print users page by page
try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()
