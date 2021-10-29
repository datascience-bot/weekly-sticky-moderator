resource "aws_ssm_parameter" "praw_client_id" {
  name        = "/${local.basename}/${var.env}/praw_client_id"
  description = "Reddit API client_id."
  type        = "SecureString"
  value       = var.praw_client_id

  tags = local.common_tags
}

resource "aws_ssm_parameter" "praw_client_secret" {
  name        = "/${local.basename}/${var.env}/praw_client_secret"
  description = "Reddit API client_secret."
  type        = "SecureString"
  value       = var.praw_client_secret

  tags = local.common_tags
}

resource "aws_ssm_parameter" "praw_username" {
  name        = "/${local.basename}/${var.env}/praw_username"
  description = "Reddit user's username."
  type        = "String"
  value       = var.praw_username

  tags = local.common_tags
}

resource "aws_ssm_parameter" "praw_password" {
  name        = "/${local.basename}/${var.env}/praw_password"
  description = "Reddit user's password."
  type        = "SecureString"
  value       = var.praw_password

  tags = local.common_tags
}
