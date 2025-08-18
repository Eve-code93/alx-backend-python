#!/bin/bash

# Activate the virtual environment
source /mnt/c/Users/USER/alxprodev/alx-backend-python/venv/bin/activate

# Override pip with a shell function that calls the correct binary
pip() {
  /mnt/c/Users/USER/alxprodev/alx-backend-python/venv/bin/pip "$@"
}

# Confirm alignment
echo "✅ Virtual environment activated with clean PATH and pip override."
echo "Python: $(which python)"
echo "Pip:    pip function now points to venv pip"
