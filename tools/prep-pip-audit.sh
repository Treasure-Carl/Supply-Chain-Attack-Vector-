#!/bin/bash
# Prepares the environment for pip-audit to run from the local cache.
# Run this once before pip-audit if the scan appears to hang.

export PIP_CACHE_DIR=/opt/pip-cache
export PIP_DISABLE_PIP_VERSION_CHECK=1

if [ ! -f /etc/pip.conf ]; then
  printf '[global]\ncache-dir = /opt/pip-cache\n' | sudo tee /etc/pip.conf > /dev/null
fi

echo "Ready. Run: pip-audit -r /opt/supply-chain/project/requirements.txt"
