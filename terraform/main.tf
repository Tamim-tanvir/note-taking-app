provider "aws" {
  region = "us-east-1"
}

resource "aws_dynamodb_table" "notes" {
  name           = "Notes"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "noteId"

  attribute {
    name = "noteId"
    type = "S"
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_lambda_function" "note_handler" {
  filename         = "lambda.zip"
  function_name    = "noteHandler"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "functions/handler.lambda_handler"
  source_code_hash = filebase64sha256("lambda.zip")
  runtime          = "python3.9"
}

resource "aws_apigatewayv2_api" "http_api" {
  name          = "note-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.note_handler.invoke_arn
}

resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /notes"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}