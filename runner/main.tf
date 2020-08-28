terraform {
  backend "s3" {
    bucket = "dvc-bench"
    key    = "terraform/config"
    region = "us-east-2"
  }
}

provider "aws" {
  region                  = var.region
  shared_credentials_file = var.aws_credentials_path
  profile                 = var.aws_profile
}

data "http" "myip" {
  url = "http://ipv4.icanhazip.com"
}

resource "aws_security_group" "ip_ssh" {
  name        = "dvc-bench-runner-ip-ssh"
  description = "Security group for the inlets server"

  /* SSH */
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${chomp(data.http.myip.body)}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "runner" {
  ami                    = "ami-0bbe28eb2173f6167"
  instance_type          = "t3a.large"
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.ip_ssh.id]
  root_block_device {
    volume_size = 40
  }
  tags = {
    Name = "dvc-bench-runner"
  }
}

resource "null_resource" "gha_runner_setup" {

  provisioner "local-exec" {
    command = "aws ec2 wait instance-running --region ${var.region} --profile ${var.aws_profile} --instance-ids ${aws_instance.runner.id}"
  }

  connection {
    type        = "ssh"
    host        = aws_instance.runner.public_dns
    user        = var.ssh_user
    private_key = file(var.private_key_path)
    timeout     = "30s"
  }

  provisioner "file" {
    source      = "setup_github_actions_runner.sh"
    destination = "/tmp/setup.sh"

  }

  provisioner "remote-exec" {
    inline = [
      "apt-get update",
      "chmod +x /tmp/setup.sh",
      "/tmp/setup.sh ${var.actions_runner_version} ${var.github_token}",
      "nohup ~/actions-runner/run.sh &",
      "sleep 1"
    ]
  }

  provisioner "local-exec" {
    command = "echo \"to connect: ssh -i '${var.private_key_path}' ${var.ssh_user}@${aws_instance.runner.public_dns}\""
  }
}
