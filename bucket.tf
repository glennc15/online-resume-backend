
resource "random_pet" "lambda_bucket_name" {
  prefix = "${var.stack_base_name}"
  length = 4
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = random_pet.lambda_bucket_name.id
}

resource "aws_s3_bucket_ownership_controls" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "lambda_bucket" {
  depends_on = [aws_s3_bucket_ownership_controls.lambda_bucket]

  bucket = aws_s3_bucket.lambda_bucket.id
  acl    = "private"
}


data "archive_file" "lambda_resume" {
  type = "zip"

  source_dir  = "${path.module}/src/api"
  output_path = "${path.module}/resume.zip"
}

resource "aws_s3_object" "lambda_get_resume" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "resume.zip"
  source = data.archive_file.lambda_resume.output_path

  etag = filemd5(data.archive_file.lambda_resume.output_path)
}
