$ErrorActionPreference = "Stop"

$clusterName = "devops-challenge"

Write-Host "Checking required tools..."

if (-not (Get-Command kind -ErrorAction SilentlyContinue)) {
    Write-Host "kind is not installed"
    exit 1
}

if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "kubectl is not installed"
    exit 1
}

if (-not (Get-Command terraform -ErrorAction SilentlyContinue)) {
    Write-Host "terraform is not installed"
    exit 1
}

Write-Host "Checking if kind cluster already exists..."
$clusters = kind get clusters

if ($clusters -contains $clusterName) {
    Write-Host "Cluster $clusterName already exists. Skipping creation."
}
else {
    Write-Host "Creating kind cluster..."
    kind create cluster --config kind/kind-config.yaml
}

Write-Host "Running Terraform..."
Push-Location terraform
terraform init
terraform apply -auto-approve
Pop-Location

Write-Host "Deploying Kubernetes manifests..."
kubectl apply -k k8s/staging

Write-Host "Waiting a few seconds before checking resources..."
Start-Sleep -Seconds 5

Write-Host "Namespace:"
kubectl get ns

Write-Host "Pods:"
kubectl get pods -n devops-challenge

Write-Host "Services:"
kubectl get svc -n devops-challenge

Write-Host "HPA:"
kubectl get hpa -n devops-challenge