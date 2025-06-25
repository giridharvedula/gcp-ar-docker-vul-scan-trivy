# Import the modules and libraries
import os
import subprocess
import json
import csv
from datetime import datetime

# start the function to run the gcloud commands
def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {cmd}\n{e.stderr.strip()}")
        return None

# check gcp artifact registry enabled or not
def check_artifact_api(project_id):
    return bool(run_cmd(f"gcloud services list --enabled --project={project_id} --filter=artifactregistry.googleapis.com --format='value(config.name)'"))

# authenticate to gcp artifact registry if it is enabled
def auth_docker():
    run_cmd("gcloud auth configure-docker --quiet")

# list the available docker repositories in gcp artifact registry
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
    print(f"📥 Pulling image: {image_reference}")
    pull_result = run_cmd(f"docker pull {image_reference}")
    if not pull_result:
        print(f" Failed to pull image: {image_reference}")
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

    detailed_rows = []
    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            detailed_rows.append({
                "CVE ID": vuln.get("VulnerabilityID", ""),
                "Pkg Name": vuln.get("PkgName", ""),
                "Installed Version": vuln.get("InstalledVersion", ""),
                "Fixed Version": vuln.get("FixedVersion", ""),
                "Severity": vuln.get("Severity", ""),
                "Title": vuln.get("Title", ""),
                "Description": vuln.get("Description", "")[:200].replace("\n", " ").replace(",", ";")
            })
    return detailed_rows

def main():
    project_id = os.getenv("PROJECT_ID")
    region = os.getenv("REGION")

    if not project_id or not region:
        print(" Please set both PROJECT_ID and REGION environment variables.")
        return

    timestamp = datetime.now().strftime("%Y%m%d")
    csv_file = f"gcp_{project_id}_audit_{timestamp}.csv"

    headers = [
        "Project ID", "Repo Name", "Image Name", "Image Reference",
        "CVE ID", "Pkg Name", "Installed Version", "Fixed Version", "Severity", "Title", "Description"
    ]
    rows = []

    auth_docker()

    print(f"\n🔍 Project: {project_id}")

    if not check_artifact_api(project_id):
        print(f" Skipping {project_id}: artifactregistry.googleapis.com not enabled.")
        return

    repos = list_repositories(project_id, region)
    if not repos:
        print(f" No repositories found in region: {region}")
        return

    for repo in repos:
        repo_name = repo["name"].split("/")[-1]
        images = list_images_in_repo(project_id, region, repo_name)
        if not images:
            print(f" No images found in repo: {repo_name}")
            continue

        seen_images = set()
        for img in images:
            image_path = img.get("package")
            if not image_path:
                continue
            image_name = image_path.split("/")[-1]
            if image_name in seen_images:
                continue  # Skip duplicate image name entries
            seen_images.add(image_name)
            image_reference = f"{region}-docker.pkg.dev/{project_id}/{repo_name}/{image_name}:latest"
            pulled_ref = pull_image(image_reference)
            if not pulled_ref:
                continue
            vuln_details = scan_image_full_details(pulled_ref)
            for vuln in vuln_details:
                rows.append({
                    "Project ID": project_id,
                    "Repo Name": repo_name,
                    "Image Name": image_name,
                    "Image Reference": image_reference,
                    **vuln
                })

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n Report exported to: {csv_file} with {len(rows)} CVE(s)")

if __name__ == "__main__":
    main()
