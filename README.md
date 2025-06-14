# GCP Artifact Registry Docker Vulnerability Scanner

A comprehensive Python script that scans all Docker repositories in a Google Cloud Platform (GCP) project and analyzes container images for security vulnerabilities using Trivy integration.

## Author

Created by Giridhar Vedula with ChatGPT assistance

## Overview

This tool automates the process of discovering and scanning Docker images stored in GCP Artifact Registry. It identifies each unique image across all repositories in your project, pulls the most recently updated version, and performs detailed vulnerability analysis using Trivy scanner.

## Features

- **Comprehensive Repository Scanning**: Automatically discovers and scans all Docker repositories in your GCP project
- **Latest Image Detection**: Identifies and analyzes the most recently updated version of every unique image
- **Trivy Integration**: Leverages Trivy's powerful vulnerability database for thorough security analysis
- **Detailed Reporting**: Exports comprehensive vulnerability findings including CVE details, affected packages, severity levels, versions, and available fixes
- **Timestamped Output**: Generates CSV reports with timestamp for easy tracking and compliance

## Script Workflow

1. **API Verification**: Confirms Artifact Registry API availability
2. **Repository Discovery**: Iterates through all Docker repositories in the project
3. **Image Identification**: Identifies unique images and their latest versions
4. **Vulnerability Scanning**: Pulls images locally and performs Trivy scans
5. **Report Generation**: Exports detailed findings to timestamped CSV file

## Prerequisites

### Required Software
- **Python 3.x**
- **Google Cloud SDK (gcloud)**
- **Docker**
- **Trivy vulnerability scanner**

### Required GCP IAM Roles
Your service account must have the following roles assigned:
- `roles/viewer`
- `roles/artifactregistry.reader`
- `roles/run.viewer`
- `roles/compute.viewer`

## Setup Instructions

### 1. Authentication
Authenticate to GCP using a service account key file:
```bash
gcloud auth activate-service-account --key-file="path/to/your-service-account-key.json"
```

### 2. Configure Docker for Artifact Registry
Set up Docker authentication for your region:
```bash
gcloud auth configure-docker us-east4-docker.pkg.dev --quiet
```
*Replace `us-east4-docker.pkg.dev` with your specific region's Artifact Registry URL*

### 3. Environment Variables
Set the required environment variables:
```bash
export REGION="your-region"           # e.g., us-east4
export PROJECT_ID="your-project-id"   # Your GCP project ID
```

## Usage

Run the scanner with:
```bash
python3 ./gcp-ar-docker-vul-scan-trivy.py
```

## Output

The script generates a comprehensive CSV report with the filename format:
```
gcp_project_audit_<PROJECT_ID>_<TIMESTAMP>.csv
```

The report includes detailed information about:
- CVE identifiers and descriptions
- Affected packages and versions
- Vulnerability severity levels
- Available fixes and remediation guidance
- Image metadata and repository information

## Security Considerations

- Ensure your service account follows the principle of least privilege
- Regularly rotate service account keys
- Store authentication credentials securely
- Review and validate scan results before taking remediation actions

## Troubleshooting

- Verify all prerequisites are installed and properly configured
- Ensure your service account has the required IAM roles
- Check that environment variables are correctly set
- Confirm Docker and Trivy are accessible from your system PATH
