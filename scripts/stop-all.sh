#!/bin/bash

# Stop all microservices and clean up

set -e

echo "🛑 Stopping all microservices..."

docker-compose down

if [ "$1" == "--clean" ]; then
    echo "🧹 Cleaning up volumes and images..."
    docker-compose down -v
    docker system prune -f
    echo "✅ Cleanup complete!"
else
    echo "✅ Services stopped!"
    echo ""
    echo "To also remove volumes and images, run:"
    echo "  ./scripts/stop-all.sh --clean"
fi
