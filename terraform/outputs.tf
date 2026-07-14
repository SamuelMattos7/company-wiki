output "access_key_id" {
  value = aws_iam_access_key.wiki_agent.id
}

output "secret_access_key" {
    value =  aws_iam_access_key.wiki_agent.secret
    sensitive = true
}

