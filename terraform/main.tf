resource "aws_s3_bucket" "wiki" {

    bucket = "research-llm-wiki"

}

resource "aws_s3_bucket_versioning" "wiki" {

    bucket = aws_s3_bucket.wiki.id

    versioning_configuration {

        status = "Enabled"

    }

}

resource "aws_s3_bucket_public_access_block" "wiki" {

    bucket = aws_s3_bucket.wiki.id

    block_public_acls       = true

    block_public_policy     = true

    ignore_public_acls      = true

    restrict_public_buckets = true

}

resource "aws_iam_policy" "wiki_access" {

    name        = "llm-wiki-access-policy"

    description = "Policy for accessing the research LLM wiki S3 bucket"

    policy      = jsonencode({

        Version = "2012-10-17"

        Statement = [

            {
                Sid      = "ListBucketOnly"
                Effect   = "Allow"
                Action   = "s3:ListBucket"
                Resource = aws_s3_bucket.wiki.arn  

            },
            {
                Sid      = "ReadWriteObjects"
                Effect   = "Allow"
                Action   = [
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                    "s3:PutObject",
                    "s3:DeleteObject"
                ]
                Resource = "${aws_s3_bucket.wiki.arn}/*"
            }

        ]

    })

}

resource "aws_iam_user" "wiki_agent" {
    name = "llm-wiki-agent"
}

resource "aws_iam_user_policy_attachment" "wiki_agent_access" {
    user       = aws_iam_user.wiki_agent.name
    policy_arn = aws_iam_policy.wiki_access.arn
}

resource "aws_iam_access_key" "wiki_agent" {
    user = aws_iam_user.wiki_agent.name
}