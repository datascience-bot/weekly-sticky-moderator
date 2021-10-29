# I'd love to move the policies to their own json, but per terraform v12 docs:
#
#     If the string you want to generate will be in JSON or YAML syntax,
#     it's often tricky and tedious to write a template that will generate
#     valid JSON or YAML that will be interpreted correctly when using lots of
#     individual interpolation sequences and directives.
#
# https://www.terraform.io/docs/configuration/functions/templatefile.html#generating-json-or-yaml-from-a-template

resource "aws_iam_user" "github" {
  name = "${var.env}.${local.basename}-lambda-deployer.github-actions"
  tags = local.common_tags
}

resource "aws_iam_access_key" "github" {
  user = aws_iam_user.github.name
}

resource "aws_iam_user_policy" "LambdaUpdateFunctionCode" {
  name = "LambdaUpdateFunctionCode"
  user = aws_iam_user.github.name

  policy = <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:UpdateFunctionCode"
      ],
      "Resource": [
        "${aws_lambda_function.main.arn}"
      ]
    }
  ]
}
EOF
}
