#!/bin/bash

# EmailAce AI Production Deployment Script

set -e

echo "🚀 Starting EmailAce AI Production Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data logs ssl

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cp env.production .env
    print_warning "Please update .env file with your production credentials before continuing."
    read -p "Press Enter after updating .env file..."
fi

# Build and start services
print_status "Building and starting services..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 30

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    print_status "✅ Services are running successfully!"
    
    # Display service information
    echo ""
    print_status "Service Information:"
    echo "  - Application: http://localhost:8000"
    echo "  - API Documentation: http://localhost:8000/docs"
    echo "  - Health Check: http://localhost:8000/api/v1/"
    echo ""
    
    # Show logs
    print_status "Recent logs:"
    docker-compose logs --tail=20
    
else
    print_error "❌ Services failed to start. Check logs:"
    docker-compose logs
    exit 1
fi

# Optional: Set up SSL certificates
read -p "Do you want to set up SSL certificates? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Setting up SSL certificates..."
    print_warning "Please place your SSL certificates in the ssl/ directory:"
    print_warning "  - ssl/cert.pem (certificate file)"
    print_warning "  - ssl/key.pem (private key file)"
    print_warning "Then uncomment the HTTPS server section in nginx.conf"
fi

print_status "🎉 Deployment completed successfully!"
print_status "Your EmailAce AI application is now running in production mode."

# Display useful commands
echo ""
print_status "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo "  - Update application: docker-compose pull && docker-compose up -d"
echo ""


