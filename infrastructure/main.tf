terraform {
  # backend "s3" {
  #   # variables must be hardcoded here
  #   bucket         = "datascience-bot-weekly-sticky-moderator-terraform-state"
  #   dynamodb_table = "datascience-bot-weekly-sticky-moderator-terraform-state-lock"
  #   encrypt        = true
  #   key            = "datascience-bot-weekly-sticky-moderator/prod/infra.tfstate"
  #   region         = "us-east-1"
  # }
  required_version = "~> 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.63"
    }
  }
}

provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}
