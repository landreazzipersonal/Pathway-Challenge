output "namespace" {
  value = kubernetes_namespace.devops.metadata[0].name
}

output "configmap_name" {
  value = kubernetes_config_map_v1.app_config.metadata[0].name
}

output "secret_name" {
  value     = kubernetes_secret_v1.app_secrets.metadata[0].name
  sensitive = true
}