## Part 2 - Infrastructure as Code and Kubernetes Kubernetes testing
- Kubernetes manifests for:
  - sample-api Deployment and Service
  - preprocessing-service Deployment and Service
  - ConfigMap
  - Secret
  - Horizontal Pod Autoscaler for both services

### Folder structure

kind/
  kind-config.yaml

terraform/
  providers.tf
  variables.tf
  main.tf
  outputs.tf

k8s/
  base/
    kustomization.yaml
    namespace.yaml
    configmap.yaml
    secret.yaml
    sample-api-deployment.yaml
    sample-api-service.yaml
    preprocessing-deployment.yaml
    preprocessing-service.yaml
    hpa-sample-api.yaml
    hpa-preprocessing.yaml
  staging/
    kustomization.yaml
  production/
    kustomization.yaml

This project includes a minimum Kubernetes and IaC setup to support local deployment and basic environment structure.

### What is included

- Terraform configuration to manage:
  - namespace
  - ConfigMap
  - Secret


## to run the deployment script, follow the instructions below:

## SHELL SCRIPT (Linux Azure CLI-Shell):
## chmod +x scripts/run-part2.sh
## ./scripts/run-part2.sh

## POWERSHELL SCRIPT (Windows or Azure CLI-Powershell):
## .\scripts\run-part2.ps1