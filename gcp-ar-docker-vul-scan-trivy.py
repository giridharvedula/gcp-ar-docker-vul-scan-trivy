def pull_image(image_reference):import os
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

def auth_docker():
  run_cmd("gcloud auth configure-docker --quiet")

def list_repositories(project_id, region):
  cmd = f"gcloud artifacts repositories list --project={project_id} --location={region} --format=json"
  output = run_cmd(cmd)
  if not output:
    return []
  return json.loads(output)

def list_images_in_repo(project_id, region, repo_name):
  cmd = f"gcloud artifacts docker images list {region}-docker.pkg.dev/{project_id}/{repo_name} --project={project_id} --format=json"
  output = run_cmd(cmd)
  if not output:
    return []
  return json.loads(output)

def pull_image(image_reference):
  print(f"Pulling image: {image_reference}")
  pull_result = run_cmd(f"docker pull {image_reference}")
  if not pull_result:
    print(f"Failed to pull image: {image_reference}")
    return None
  return image_reference

def scan_image_full_details(image_url):
  print(f" Scanning image with Trivy: {image_url}")
  output = run_cmd(f"trivy image --quiet --format json {image_url}")
  if not output:
    print(" Trivy returned no output.")
    return []
  try:
    data = json.loads(output)
  except json.JSONDecodeError:
    print(" Failed to parse Trivy JSON.")
    return []

