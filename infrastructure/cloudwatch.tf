resource "aws_cloudwatch_event_rule" "trigger" {
  name                = "${var.env}-${local.basename}-trigger"
  description         = "Trigger every Sunday at 12:00 UTC"
  schedule_expression = "cron(0 12 ? * SUN *)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.trigger.name
  target_id = "SendToLambda"
  arn       = aws_lambda_function.main.arn
}
