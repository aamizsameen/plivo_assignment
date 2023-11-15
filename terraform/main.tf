
module "eks_cluster" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 19.0"
  cluster_name    = "my-eks-cluster"
  subnet_ids      = ["subnet-0aec618be9b082992", "subnet-03df0e8dcfad5c160"]
  vpc_id          = "vpc-066e059e1f2d43195"
  cluster_version = "1.26"
}


module "eks_node_group" {
  source          = "terraform-aws-modules/eks/aws//modules/eks-managed-node-group"
  cluster_name    = "my-eks-cluster"
  name            = "my-node-group1"
  subnet_ids      = ["subnet-0aec618be9b082992", "subnet-03df0e8dcfad5c160"]
  instance_types   = ["t3.medium"]
  desired_size     = 2
  min_size     = 1
  max_size     = 3
}