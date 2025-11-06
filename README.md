# age-calculator-api
Flask Age Calculator API deployed on AWS EC2 with Docker

# 🚀 Dockerizing a Flask App on AWS EC2: Full Guide

This guide covers launching an AWS EC2 instance, SSH access, installing Docker and Python, creating a simple Flask app (age calculator API), building and pushing a Docker image to Docker Hub, pulling it back, running the container, and accessing it via terminal or browser. Based on hands-on steps for learning containerization.

---

## 🧩 1. Prerequisites
- AWS account with IAM user having EC2 access.
- Local machine with AWS CLI configured (see separate guide for that).
- Basic terminal knowledge.

Ensure AWS CLI is ready:

```bash
aws --version
```

If not, install and configure it first.

---

## 🌐 2. Launch AWS EC2 Instance
Launch a Ubuntu-based virtual server.

1. Go to AWS Console > EC2 > Launch Instance.
2. **AMI**: Ubuntu Server 24.04 LTS.
3. **Instance Type**: t3.micro (free tier).
4. **Key Pair**: Create new (e.g., "docker-key.pem") and download.
5. **Security Group**: Allow SSH (22), HTTP (80), and TCP 5000 from Anywhere (for testing).
6. Launch and note the Public IP (e.g., 172.31.3.151).

Verify:

```bash
aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress"
```

---

## 🔑 3. SSH into the Instance
Connect remotely to control the server.

From local terminal:

```bash
chmod 400 docker-key.pem
ssh -i docker-key.pem ubuntu@<PUBLIC-IP>
```

Example: `ssh -i docker-key.pem ubuntu@172.31.3.151`

Inside: Update system:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🛠️ 4. Install Docker and Python
Set up tools for containerization and app development.

Install Docker:

```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

Logout and SSH back in. Test: `docker run hello-world`.

Install Python (if needed):

```bash
sudo apt install python3-pip -y
```

---

## 📝 5. Create App Files
Build a simple Flask API (e.g., age calculator).

Create directory:

```bash
mkdir -p /var/www/html/python-mini-projects/projects/agecalc
cd /var/www/html/python-mini-projects/projects/agecalc
```

`app.py` (using nano):

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Age API!"

@app.route('/calculate')
def calculate():
    name = request.args.get('name', 'User')
    age = request.args.get('age', '0')
    return f"Hello {name}! You are {age} years old."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

`Dockerfile`:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 🏗️ 6. Build, Tag, and Push Image
Create and upload the container image to Docker Hub.

Build:

```bash
docker build -t age-api .
```

Tag (replace mahmeddev with your Docker Hub username):

```bash
docker tag age-api mahmeddev/age-api:dev
```

Push (login first: `docker login`):

```bash
docker push mahmeddev/age-api:dev
```

---

## 📥 7. Pull and Run the Container
Fetch and deploy the image.

Pull:

```bash
docker pull mahmeddev/age-api:dev
```

Run:

```bash
docker run -p 5000:5000 mahmeddev/age-api:dev
```

Check ports: `ss -tuln | grep 5000`

---

## 🌐 8. Access the App
Test from terminal or browser.

From EC2 terminal:

```bash
curl http://localhost:5000
curl "http://localhost:5000/calculate?name=Ahmed&age=25"
```

From browser: `http://<PUBLIC-IP>:5000` or `http://<PUBLIC-IP>:5000/calculate?name=Ahmed&age=25`

Example logs show successful access.

---

## 🧹 9. Cleanup and Tips
- Stop container: `docker stop <CONTAINER-ID>` (from `docker ps`).
- Remove: `docker system prune -a`.
- Stop EC2: AWS Console > Instances > Stop/Terminate.
- For production: Use HTTPS, persistent storage, and ECR instead of Docker Hub.
- Common issues: Port conflicts? Change with `-p 8080:5000`. Permissions? Relogin after usermod.

---

## ✅ Quick Commands Recap
| Purpose | Command |
|---------|---------|
| SSH In | `ssh -i key.pem ubuntu@IP` |
| Install Docker | `sudo apt install docker.io -y` |
| Build Image | `docker build -t age-api .` |
| Push | `docker push username/image:tag` |
| Run | `docker run -p 5000:5000 image:tag` |
| Access | `curl http://localhost:5000` |
