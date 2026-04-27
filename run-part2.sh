# Bash script

Create a file like `scripts/run-part2.sh`:

```bash
#!/usr/bin/env bash

set -e

CLUSTER_NAME="devops-challenge"

echo "Checking required tools..."
command -v kind >/dev/null 2>&1 || { echo "kind is not installed"; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "kubectl is not installed"; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo "terraform is not installed"; exit 1; }

echo "Checking if kind cluster already exists..."
if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
  echo "Cluster ${CLUSTER_NAME} already exists. Skipping creation."
else
  echo "Creating kind cluster..."
  kind create cluster --config kind/kind-config.yaml
fi

echo "Running Terraform..."
cd terraform
terraform init
terraform apply -auto-approve
cd ..

echo "Deploying Kubernetes manifests..."
kubectl apply -k k8s/staging

echo "Waiting a few seconds before checking resources..."
sleep 5

echo "Namespace:"
kubectl get ns

echo "Pods:"
kubectl get pods -n devops-challenge

echo "Services:"
kubectl get svc -n devops-challenge

echo "HPA:"
kubectl get hpa -n devops-challenge || true

echo "Done."