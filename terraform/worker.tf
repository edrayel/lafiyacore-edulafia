resource "aws_ecs_task_definition" "worker" {
  family                   = "edulafia-worker-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "edulafia-worker"
      image     = "ghcr.io/edward_rajah/lafiyacore-edulafia/backend:${var.image_tag}"
      essential = true
      command   = ["python", "-m", "arq", "edulafia.worker.WorkerSettings"]
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
          awslogs-group         = "/ecs/edulafia-worker-${var.environment}"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
          awslogs-create-group  = "true"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "worker" {
  name            = "edulafia-worker-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.worker.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = false
  }
}
