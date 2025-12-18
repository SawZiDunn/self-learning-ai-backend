#!/bin/bash
# Quick deployment script for AWS App Runner

set -e

echo "🚀 Self-Learning AI - AWS Deployment Script"
echo ""

# Check Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Get Docker Hub username
read -p "Enter your Docker Hub username: " DOCKER_USER
IMAGE_NAME="$DOCKER_USER/self-learning-ai"

echo ""
echo "📦 Building Docker image..."
docker build -t self-learning-ai .

echo ""
echo "🏷️  Tagging image as $IMAGE_NAME:latest"
docker tag self-learning-ai:latest $IMAGE_NAME:latest

echo ""
echo "🔐 Please login to Docker Hub"
docker login

echo ""
echo "⬆️  Pushing to Docker Hub..."
docker push $IMAGE_NAME:latest

echo ""
echo "✅ Image pushed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Go to AWS Console → App Runner"
echo "2. Create new service"
echo "3. Select 'Container registry' → 'Docker Hub'"
echo "4. Enter image: $IMAGE_NAME:latest"
echo "5. Set port: 5000"
echo "6. Add environment variables:"
echo "   - GROQ_API_KEY"
echo "   - SUPABASE_URL"
echo "   - SUPABASE_KEY"
echo "7. Deploy!"
echo ""
echo "🌐 Your API will be live at: https://[random-id].awsapprunner.com"
