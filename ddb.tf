# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

resource "aws_dynamodb_table" "users_table" {
  name           = "${var.stack_base_name}_Resumes"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "userid"

  attribute {
    name = "userid"
    type = "S"
  }
}

# output "users_table" {
#   value = aws_dynamodb_table.users_table.id
# }
