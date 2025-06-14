import os
import subprocess
import json
import csv
from date import datetime

def run_cmd(cmd):
  try:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
    return result.stdout.strip()
  except subprocess.CalledProcessError as e:
    print(f"[ERROR] {cmd}\n{e.stderr.strip()}")
    return None

