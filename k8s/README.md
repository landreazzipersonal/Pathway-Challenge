# Kubernetes (k8s)

This folder contains Kubernetes manifests to deploy the project services:

- sample-api (port 5000)
- preprocessing-service (port 5001)

The manifests are organized using a `base/` layer and environment overlays (`staging/`, `production/`).

## Structure

text

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
