resource "random_password" "couchdb_password" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_ecs_task_definition" "couchdb" {
  family                   = "edulafia-couchdb-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "edulafia-couchdb"
      image     = "couchdb:3"
      essential = true
      portMappings = [
        {
          containerPort = 5984
          hostPort      = 5984
        }
      ]
      environment = [
        { name = "COUCHDB_USER", value = "admin" },
        { name = "COUCHDB_PASSWORD", value = random_password.couchdb_password.result }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/edulafia-couchdb-${var.environment}"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
          awslogs-create-group  = "true"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "couchdb" {
  name            = "edulafia-couchdb-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.couchdb.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = false
  }
}
