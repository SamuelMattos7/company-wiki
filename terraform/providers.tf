terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}
variable "existing_role_name" {
  description = "Existing role to attach the S3 access policy to. Leave unset when access is managed separately."
  type        = string
  default     = null
}
