output "github_actions_requirements" {
  value = {
    aws_access_key_id     = aws_iam_access_key.github.id
    aws_secret_access_key = aws_iam_access_key.github.secret
    lambda_function_arn   = aws_lambda_function.main.arn
  }
  sensitive = true
}
