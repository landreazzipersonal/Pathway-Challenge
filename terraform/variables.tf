variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "devops-challenge"
}

variable "app_env" {
  description = "Application environment"
  type        = string
  default     = "staging"
}

variable "debug" {
  description = "Debug flag"
  type        = string
  default     = "false"
}

variable "sample_api_port" {
  description = "Sample API port"
  type        = string
  default     = "5000"
}

variable "preprocessing_port" {
  description = "Preprocessing service port"
  type        = string
  default     = "5001"
}

variable "api_key" {
  description = "Example secret value"
  type        = string
  sensitive   = true
  default     = "change-me"
}