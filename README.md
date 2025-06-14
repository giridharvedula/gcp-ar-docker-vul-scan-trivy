# gcp-ar-docker-vul-scan-trivy.py #
# -------------------------------------------------------------------------------------------
# GCP Artifact Registry Project Scanner with Trivy Integration
# Scans all Docker repositories in a GCP project, identifies each unique image, and analyzes
# the most recently updated version of every image for vulnerabilities using Trivy.
#
# Author: Giridhar Vedula + ChatGPT
#
# Features:
#   - Retrieves the latest digest for each unique image across all repositories.
#   - Performs local vulnerability scans with Trivy and exports comprehensive results.
#   - Outputs findings to a timestamped CSV file.
#
# Script Workflow:
#   - Verifies Artifact Registry API availability.
#   - Iterates through all Docker repositories and images.
#   - For each image, pulls the most recent version and scans with Trivy.
#   - Exports a detailed vulnerability report (CVE, package, severity, version, fix, etc.) to CSV.
#
# Prerequisites:
#   - Python 3.x
#   - gcloud SDK
#   - Docker
#   - Trivy
#
# Required GCP Roles for Service Account:
#   - roles/viewer
#   - roles/artifactregistry.reader
#   - roles/run.viewer
#   - roles/compute.viewer
#
# Setup Instructions:
#   1. Authenticate to GCP with a service account key file:
#        gcloud auth activate-service-account --key-file="path/to/key.json"
#   2. Configure Docker for Artifact Registry:
#        gcloud auth configure-docker us-east4-docker.pkg.dev --quiet
#   3. Set environment variables:
#        export REGION="your-region"   # e.g., us-east4
#        export PROJECT_ID="your-project-id"
#
# Usage:
#   python3 ./gcp-ar-docker-vul-scan-trivy.py
#   Output: gcp_project_audit_<PROJECT_ID>_<TIMESTAMP>.csv
# -------------------------------------------------------------------------------------------
