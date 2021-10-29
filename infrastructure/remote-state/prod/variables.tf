variable "aws_profile" {
  description = "The aws profile used to terraform the infrastructure."
  sensitive   = true
  type        = string
}

variable "aws_region" {
  description = "The aws region where the infrastructure is deployed."
  sensitive   = true
  type        = string
}

variable "env" {
  description = "The deployment environment."
  default     = "dev"
}

locals {
  basename = "datascience-bot"
  common_tags = {
    environment = var.env
    project     = local.basename
  }
}
