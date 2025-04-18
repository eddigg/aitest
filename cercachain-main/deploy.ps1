param(
    [string]$Environment = "development"
)

Write-Host "Starting deployment for $Environment environment..."

# Create and activate Python virtual environment
Write-Host "Setting up Python environment..."
if (-not (Test-Path "api\venv")) {
    python -m venv api\venv
}
. .\api\venv\Scripts\Activate

# Install Python dependencies
Write-Host "Installing backend dependencies..."
pip install -r api\requirements.txt

# Start backend server in a new window
Write-Host "Starting backend server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd api; .\venv\Scripts\python main.py"

# Install and start frontend
Write-Host "Setting up frontend..."
Set-Location frontend
npm install
Write-Host "Starting frontend development server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start"
Set-Location ..

Write-Host "Deployment complete!"
Write-Host "Frontend running at: http://localhost:3000"
Write-Host "Backend running at: http://localhost:8000"