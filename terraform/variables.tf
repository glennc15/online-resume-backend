# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

# Input variable definitions

variable "aws_region" {
  description = "AWS region for all resources."
  type    = string
  default = "us-east-1"
}

variable "stack_base_name" {
    default = "online-resume"
}
variable "lambda_memory" {
  default = "128"
}
variable "lambda_runtime" {
  default = "python3.9"
}
variable "lambda_timeout" {
  default = "100"
}
variable "lambda_tracing_config" {
  default = "Active"
}