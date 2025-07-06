#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

# Print filtered users (age > 25) in a batch of 50
try:
    for user in processing.batch_processing(50):
        print(user)
except BrokenPipeError:
    sys.stderr.close()
