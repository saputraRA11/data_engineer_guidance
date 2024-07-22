variable "credantials" {
  description = "credentials name"
  default = "./keys/credentials.json"
}
variable "project" {
  description = "Project name"
}

variable "region" {
  description = "Region name"
}

variable "aws_s3_bucket" {
    description="S3 Bucket Name"
    default="terra-bucket-v3"
}

variable "pubsub_topic_name" {
    description=""
    default="terra-bucket-v3"
}

variable "aws_access_key" {
    description="AWS Access key"
    default="terra-bucket-v3"
}

variable "aws_secret_key" {
    description="AWS Secret key"
    default="terra-bucket-v3"
}