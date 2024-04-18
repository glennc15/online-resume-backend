# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

# provider "aws" {
#   region = var.aws_region

# }



terraform {
  backend "remote" {
    organization = "online-resume-backend"
    workspaces {
      name = "online-resume-backend-workspace"
    }
  }
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}






resource "aws_lambda_function" "get_resume" {
  function_name = "GetResume"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_get_resume.key

  runtime = "python3.9"
  handler = "resume.resume_handler"

  source_code_hash = data.archive_file.lambda_resume.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
}

resource "aws_cloudwatch_log_group" "get_resume" {
  name = "/aws/lambda/${aws_lambda_function.get_resume.function_name}"

  retention_in_days = 30
}

resource "aws_iam_role" "lambda_exec" {
  name = "serverless_lambda"
  description = "Lambda function IAM role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


resource "aws_iam_policy" "userfunctions_lambda_role_policy" {
  name        = "${var.stack_base_name}_userfunctions_lambda_role_policy"
  description = "Lambda function policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:DeleteItem",
        "dynamodb:PutItem",
        "dynamodb:Scan",
        "dynamodb:Query",
        "dynamodb:UpdateItem",
        "dynamodb:BatchWriteItem",
        "dynamodb:BatchGetItem",
        "dynamodb:DescribeTable",
        "dynamodb:ConditionCheckItem"
      ],
      "Effect": "Allow",
      "Resource": "arn:*:dynamodb:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_dynamodb_table.resume_table.id}"
    },
    {
      "Action": [
        "logs:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Action": [
        "xray:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "userfunctions_lambda_attach" {
  name       = "${var.stack_base_name}_userfunctions_lambda_attachment"
  roles      = [aws_iam_role.lambda_exec.name]
  policy_arn = aws_iam_policy.userfunctions_lambda_role_policy.arn
}


resource "aws_apigatewayv2_api" "lambda" {
  name          = "serverless_lambda_gw"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  name        = "serverless_lambda_stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "get_resume" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.get_resume.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_resume" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "GET /resume"
  target    = "integrations/${aws_apigatewayv2_integration.get_resume.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

  retention_in_days = 30
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_resume.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}
