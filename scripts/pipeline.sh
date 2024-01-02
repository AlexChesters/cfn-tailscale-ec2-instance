set -e

aws cloudformation deploy \
  --template-file ci/codepipeline.yml \
  --stack-name codepipeline-cfn-tailscale-ec2-instance \
  --capabilities CAPABILITY_IAM \
  --region eu-west-1 \
  --profile service-catalog
