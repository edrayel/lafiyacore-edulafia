resource "aws_ecs_task_definition" "migrate" {
  family                   = "edulafia-migrate-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "edulafia-migrate"
      image     = "ghcr.io/edward_rajah/lafiyacore-edulafia/backend:${var.image_tag}"
      essential = true
      command   = ["uv", "run", "alembic", "upgrade", "head"]
      environment = [
        { name = "ENVIRONMENT", value = var.environment }
      ]
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = "${aws_secretsmanager_secret.app_secrets.arn}:DATABASE_URL::"
        },
        {
          name      = "REDIS_URL"
          valueFrom = "${aws_secretsmanager_secret.app_secrets.arn}:REDIS_URL::"
        },
        {
          name      = "APP_SECRET_KEY"
          valueFrom = "${aws_secretsmanager_secret.app_secrets.arn}:APP_SECRET_KEY::"
        },
        {
          name      = "JWT_SECRET_KEY"
          valueFrom = "${aws_secretsmanager_secret.app_secrets.arn}:JWT_SECRET_KEY::"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/edulafia-migrate-${var.environment}"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
          awslogs-create-group  = "true"
        }
      }
    }
  ])
}

# Add IAM policy to execution role to allow reading secrets
resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "edulafia-ecs-execution-secrets-${var.environment}"
  role = aws_iam_role.ecs_task_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          aws_secretsmanager_secret.db_credentials.arn,
          aws_secretsmanager_secret.app_secrets.arn
        ]
      }
    ]
  })
}

output "private_subnets" {
  value = module.vpc.private_subnets
}

output "ecs_sg_id" {
  value = aws_security_group.ecs_sg.id
}