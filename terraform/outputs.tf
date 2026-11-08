output "bucket_name" {
  value = aws_s3_bucket.wiki.id
}

output "wiki_access_policy_arn" {
  value = aws_iam_policy.wiki_access.arn
}
