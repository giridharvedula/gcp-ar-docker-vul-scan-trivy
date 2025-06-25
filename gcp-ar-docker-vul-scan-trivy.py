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

def check_artifact_api(project_id):
  return bool(run_cmd(f"gcloud services list --enabled --project={project_id} --filter=artifactregistry.googleapis.com --format='value(config.name)'"))
