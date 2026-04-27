SHELL := /bin/bash

CLUSTER_NAME ?= devops-challenge
NAMESPACE    ?= devops-challenge
ENV          ?= staging

K8S_DIR      := k8s/$(ENV)
KIND_CONFIG  := kind/kind-config.yaml

SAMPLE_IMAGE ?= sample-api
PREP_IMAGE   ?= preprocessing-service
SAMPLE_TAG   ?= $(ENV)
PREP_TAG     ?= $(ENV)

.PHONY: help check-tools kind-create kind-delete docker-build kind-load \
        tf-init tf-apply tf-destroy \
        k8s-apply k8s-delete \
        wait status logs port-forward-api port-forward-grafana \
        deploy destroy

help:
    @echo "Targets:"
    @echo "  make check-tools               - Check required tools exist"
    @echo "  make kind-create               - Create kind cluster"
    @echo "  make kind-delete               - Delete kind cluster"
    @echo "  make docker-build              - Build local Docker images"
    @echo "  make kind-load                 - Load local images into kind"
    @echo "  make tf-init                   - Terraform init"
    @echo "  make tf-apply                  - Terraform apply"
    @echo "  make tf-destroy                - Terraform destroy"
    @echo "  make k8s-apply ENV=staging     - Apply kustomize overlay"
    @echo "  make k8s-delete ENV=staging    - Delete kustomize overlay"
    @echo "  make wait                      - Wait for deployments to be ready"
    @echo "  make status                    - Show pods/services/hpa"
    @echo "  make logs APP=sample-api       - Tail logs for one app"
    @echo "  make deploy ENV=staging        - End-to-end: kind + build + load + tf + k8s"
    @echo "  make destroy ENV=staging       - Remove k8s + tf (cluster kept), or use kind-delete"
    @echo ""
    @echo "Variables:"
    @echo "  ENV=staging|production (default: staging)"
    @echo "  CLUSTER_NAME=devops-challenge"
    @echo "  NAMESPACE=devops-challenge"

check-tools:
    @command -v kind >/dev/null 2>&1 || (echo "Missing: kind" && exit 1)
    @command -v kubectl >/dev/null 2>&1 || (echo "Missing: kubectl" && exit 1)
    @command -v terraform >/dev/null 2>&1 || (echo "Missing: terraform" && exit 1)
    @command -v docker >/dev/null 2>&1 || (echo "Missing: docker" && exit 1)
    @echo "All required tools found."

kind-create: check-tools
    @if kind get clusters | grep -q "^$(CLUSTER_NAME)$$"; then \
        echo "kind cluster $(CLUSTER_NAME) already exists"; \
    else \
        echo "Creating kind cluster $(CLUSTER_NAME)"; \
        kind create cluster --name $(CLUSTER_NAME) --config $(KIND_CONFIG); \
    fi

kind-delete: check-tools
    @echo "Deleting kind cluster $(CLUSTER_NAME)"
    @kind delete cluster --name $(CLUSTER_NAME)

docker-build: check-tools
    @echo "Building images..."
    @docker build -t $(SAMPLE_IMAGE):latest ./sample-api
    @docker build -t $(PREP_IMAGE):latest ./preprocessing-service
    @echo "Tagging images for ENV=$(ENV)..."
    @docker tag $(SAMPLE_IMAGE):latest $(SAMPLE_IMAGE):$(SAMPLE_TAG)
    @docker tag $(PREP_IMAGE):latest $(PREP_IMAGE):$(PREP_TAG)

kind-load: check-tools
    @echo "Loading images into kind cluster $(CLUSTER_NAME)..."
    @kind load docker-image $(SAMPLE_IMAGE):$(SAMPLE_TAG) --name $(CLUSTER_NAME)
    @kind load docker-image $(PREP_IMAGE):$(PREP_TAG) --name $(CLUSTER_NAME)

tf-init: check-tools
    @echo "Terraform init..."
    @cd terraform && terraform init

tf-apply: tf-init
    @echo "Terraform apply..."
    @cd terraform && terraform apply -auto-approve

tf-destroy: tf-init
    @echo "Terraform destroy..."
    @cd terraform && terraform destroy -auto-approve

k8s-apply: check-tools
    @echo "Applying kustomize overlay: $(K8S_DIR)"
    @kubectl apply -k $(K8S_DIR)

k8s-delete: check-tools
    @echo "Deleting kustomize overlay: $(K8S_DIR)"
    @kubectl delete -k $(K8S_DIR) --ignore-not-found

wait: check-tools
    @echo "Waiting for deployments in namespace $(NAMESPACE)..."
    @kubectl rollout status deployment/sample-api -n $(NAMESPACE) --timeout=120s
    @kubectl rollout status deployment/preprocessing-service -n $(NAMESPACE) --timeout=120s

status: check-tools
    @echo "Namespace: $(NAMESPACE)"
    @kubectl get pods -n $(NAMESPACE)
    @kubectl get svc -n $(NAMESPACE)
    @kubectl get hpa -n $(NAMESPACE) 2>/dev/null || true

logs: check-tools
    @if [ -z "$(APP)" ]; then \
        echo "Usage: make logs APP=sample-api"; exit 1; \
    fi
    @kubectl logs -n $(NAMESPACE) -l app=$(APP) --tail=100 -f

deploy: kind-create docker-build kind-load tf-apply k8s-apply wait status
    @echo "Deploy completed for ENV=$(ENV)."

destroy: k8s-delete tf-destroy
    @echo "Destroyed k8s resources + terraform-managed resources for ENV=$(ENV)."
    @echo "If you want to delete the cluster too: make kind-delete"
``
