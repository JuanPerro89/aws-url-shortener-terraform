resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}

resource "aws_iam_role" "github_plan" {
  name = "github-actions-terraform-plan"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRoleWithWebIdentity"
      Principal = { Federated = aws_iam_openid_connect_provider.github.arn }
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = [
            "repo:JuanPerro89/aws-url-shortener-terraform:pull_request",
            "repo:JuanPerro89/aws-url-shortener-terraform:ref:refs/heads/master",
          ]
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "github_plan" {
  name = "terraform-plan-readonly"
  role = aws_iam_role.github_plan.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["dynamodb:Describe*", "dynamodb:List*", "iam:Get*", "iam:List*", "lambda:Get*", "lambda:List*"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "s3:ListBucket"
        Resource = "arn:aws:s3:::tfstate-url-shortener-1989322048"
      },
      {
        Effect   = "Allow"
        Action   = "s3:GetObject"
        Resource = "arn:aws:s3:::tfstate-url-shortener-1989322048/url-shortener/v2/terraform.tfstate"
      },
    ]
  })
}

output "ci_role_arn" {
  value = aws_iam_role.github_plan.arn
}
