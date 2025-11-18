@echo off
echo ========================================
echo Starting Docker Deployment Test
echo ========================================
echo.

echo Step 1: Starting PostgreSQL with Docker Compose...
docker-compose up -d

echo.
echo Step 2: Waiting for services to be ready...
timeout /t 5 /nobreak > nul

echo.
echo Step 3: Running deployment tests...
python test_docker_deployment.py

echo.
echo ========================================
echo Test completed!
echo ========================================
echo.
echo To stop Docker containers, run: docker-compose down
echo To view logs, run: docker-compose logs
pause
