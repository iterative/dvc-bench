variable "aws_profile" {
  description = "AWS profile name"
}
variable "aws_credentials_path" {
  description = "Path to AWS credentials"
}
variable "github_token" {
  description = "Github actions token from https://github.com/iterative/dvc-bench/settings/actions/add-new-runner"
}
variable "key_name" {
  description = "Name of your SSH key pair in Amazon EC2."
}
variable "private_key_path" {
  description = "Path to the private SSH key (.pem), used to access the instance."
}
variable "ssh_user" {
  description = "SSH user name to connect to your instance."
}
variable "region" {
  description = "Region of our instance"
}
variable "actions_runner_version" {
  description = "Latest version of actions runner from https://github.com/actions/runner/releases/latest (omit 'v')"
}
