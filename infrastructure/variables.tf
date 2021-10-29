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

variable "praw_client_id" {
  description = "Reddit API client id."
  sensitive   = true
  type        = string
}

variable "praw_client_secret" {
  description = "Reddit API client secret."
  sensitive   = true
  type        = string
}

variable "praw_password" {
  description = "Reddit user's password."
  sensitive   = true
  type        = string
}

variable "praw_username" {
  description = "Reddit user's username."
  type        = string
}


locals {
  basename = "datascience-bot"
  common_tags = {
    environment = var.env
    project     = local.basename
  }
}
