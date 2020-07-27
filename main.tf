resource "aws_instance" "practice_instance" {

  ami           = "ami-0732b62d310b80e97"
  instance_type = "t2.micro"
  tags = {
    name ="terraform" 
   }
}
