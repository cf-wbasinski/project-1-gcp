# Cloud Run Deployment Task

This document outlines the steps required to deploy a Flask application to Google Cloud Run. It assumes you have a basic understanding of GCP and Docker.

## Prerequisites

- A Google Cloud Project.
- The `gcloud` CLI installed and configured.
- Docker installed.
- Basic knowledge of Git.
- The source code of the application available in a Git repository.

## Deployment Steps

### 1. Enable Cloud Run API

- Enable the Cloud Run API for your project.

### 2. Configure Service Account

1.  Navigate to **IAM & Admin** > **Service Accounts** in the GCP console.
2.  Create a new service account.
3.  Grant the necessary roles to the service account:
    - **Vertex AI Platform Express User**
4.  Grant yourself the **Service Account User** role on this service account to allow impersonation.

### 3. Build and Push Docker Image

1.  Open Cloud Shell or your local terminal.
2.  Clone the application's repository.
3.  Build the Docker image, specifying your desired image name and tag.
4.  Push the image to the Google Container Registry.

### 4. Set up Secrets

1.  Go to **Secret Manager** in the GCP console.
2.  Create a new secret for each sensitive configuration value.
3.  Add a secret version with the actual value for each secret.

### 5. Configure Logging

- Review your application's logging setup, typically within the application's code.

### 6. Deploy to Cloud Run

- Use the `gcloud run deploy` command to deploy the application to Cloud Run, specifying:
  - The service name.
  - The Docker image.
  - The platform as managed.
  - The GCP region.
  - That unauthenticated access is not allowed.
  - The service account.
  - Secrets to be injected into the environment.
  - Environment variables.

### 7. Post-Deployment Updates

After the deployment is complete, you can adjust the service's scaling and concurrency settings.

#### a. Set up Scaling

- Update the service to configure minimum and maximum instances.

#### b. Set up Concurrency

- Update the service to configure the concurrency setting.

#### c. Set up Timeout

- Update the service to configure the request timeout.

#### d. Service Summary

- Describe the service to view its details, including the URL.

### 8. Invoke the API

#### a. Check Invoker Role

- Verify that your service account has the invoker role.

#### b. Grant Token Creator Permission

- Grant the **Service Account Token Creator** role to your user account.

#### c. Generate Access Token

- Generate an access token for the service account.

#### d. Call the API

- Use `curl` to call the API with the generated token, providing a test question.

# Kubernetes Deployment Task (Private GKE Cluster)

This document outlines the steps required to deploy an application to a private Google Kubernetes Engine (GKE) cluster. It assumes you have a basic understanding of GCP, Kubernetes, and Docker.

## Prerequisites

- A Google Cloud Project.
- The `gcloud` CLI installed and configured.
- `kubectl` installed.
- Basic knowledge of Git.
- The source code of the application containerized as a Docker image.

## Deployment Steps

### 1. Set Up Your Environment

- Ensure you have the Google Cloud SDK installed and authenticated.
- Define necessary environment variables (e.g., project ID, region, zone, network names, cluster name, service account details, namespace).

### 2. Create a Private VPC with Private Google Access

- Create a VPC network.
- Create a private subnet within the VPC, enabling private Google access.

### 3. Enable NAT for Private Cluster to Pull Images

- Create a Cloud Router in the VPC.
- Create a NAT configuration for the router, allowing the private GKE cluster to pull images from GCR.

### 4. Create the Private GKE Cluster

    *   Create a private GKE cluster with the following specifications:
        *   IP aliasing enabled.
        *   Using the created VPC and subnet.
        *   Private nodes enabled.
        *   Master authorized networks enabled.
        *   Auto-repair enabled.
        *   A regular release channel.

- Fetch the cluster credentials.

### 5. Deploy the Application

1.  Create a Kubernetes namespace for the application.
2.  Create a Kubernetes service account within the namespace.
3.  Create an IAM service account.
4.  Grant the necessary IAM permissions to the service account, including:
    - Storage Object Viewer role.
    - Workload Identity User role.

### 6. Create Kubernetes Deployment

- Define a Kubernetes Deployment YAML file specifying:
  - The number of replicas.
  - The application's image.
  - The container ports.
  - Environment variables.
  - The service account to be used.
- Apply the deployment.

### 7. Expose the Application

- Define a Kubernetes Service YAML file specifying:
  - The service type as LoadBalancer.
  - Annotations for an internal load balancer.
  - The port mapping.
- Apply the service.

### 8. Test Private Google Access

1.  Create a Compute Engine VM instance within the same VPC and subnet as the GKE cluster (without a public IP).
2.  Create a firewall rule to allow the VM to access the GKE cluster.
3.  SSH into the VM.
4.  Install `curl`.
5.  Retrieve the service's internal IP address.
6.  Use `curl` to test the application's endpoint.

### 9. Clean Up

- Delete the GKE cluster.
- Delete the test VM instance.
- Delete the firewall rule.
- Delete the VPC network.
