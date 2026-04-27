resource "kubernetes_namespace" "devops" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_config_map_v1" "app_config" {
  metadata {
    name      = "app-config"
    namespace = kubernetes_namespace.devops.metadata[0].name
  }

  data = {
    APP_ENV        = var.app_env
    DEBUG          = var.debug
    SAMPLE_API_PORT = var.sample_api_port
    PREPROCESS_PORT = var.preprocessing_port
    PREPROCESS_URL  = "http://preprocessing-service:${var.preprocessing_port}/preprocess"
  }
}

resource "kubernetes_secret_v1" "app_secrets" {
  metadata {
    name      = "app-secrets"
    namespace = kubernetes_namespace.devops.metadata[0].name
  }

  type = "Opaque"

  data = {
    API_KEY = var.api_key
  }
}