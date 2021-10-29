resource "aws_lambda_function" "main" {
  function_name = "${var.env}-${local.basename}"
  role          = aws_iam_role.lambda_runner.arn
  runtime       = "python3.8"
  handler       = "main.handler"
  filename      = "data/helloworld.zip"

  timeout                        = 60
  reserved_concurrent_executions = 1

  environment {
    variables = {
      SSM_PRAW_CLIENT_ID     = aws_ssm_parameter.praw_client_id.name
      SSM_PRAW_CLIENT_SECRET = aws_ssm_parameter.praw_client_secret.name
      SSM_PRAW_USERNAME      = aws_ssm_parameter.praw_username.name
      SSM_PRAW_PASSWORD      = aws_ssm_parameter.praw_password.name
    }
  }

  tags = local.common_tags
}

resource "aws_iam_role" "lambda_runner" {
  name = "${var.env}.${local.basename}.lambda_runner"
  tags = local.common_tags

  assume_role_policy = <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Action": "sts:AssumeRole",
          "Effect": "Allow",
          "Principal": {
              "Service": "lambda.amazonaws.com"
          }
      }
  ]
}
EOF
}

resource "aws_iam_policy" "access_param_store" {
  name        = "access-param-store-policy"
  description = "Access relevant parameters in param store."
  tags        = local.common_tags

  policy = <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:GetParametersByPath"
      ],
      "Effect": "Allow",
      "Resource": [
        "${aws_ssm_parameter.praw_client_id.arn}",
        "${aws_ssm_parameter.praw_client_secret.arn}",
        "${aws_ssm_parameter.praw_username.arn}",
        "${aws_ssm_parameter.praw_password.arn}"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_ssm_access" {
  role       = aws_iam_role.lambda_runner.name
  policy_arn = aws_iam_policy.access_param_store.arn
}

data "aws_caller_identity" "current" {
  # Retrieves information about the AWS account corresponding to the
  # access key being used to run Terraform, which we need to populate
  # the "source_account" on the permission resource.
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id   = "AllowExecutionFromCloudWatch"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.main.function_name
  principal      = "events.amazonaws.com"
  source_account = data.aws_caller_identity.current.account_id
  source_arn     = aws_cloudwatch_event_rule.trigger.arn
}
