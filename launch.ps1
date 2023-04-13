# Start Flask server in background
cd backend/src/
Start-Process -FilePath "python" -ArgumentList "main.py" -WindowStyle Hidden
$FLASK_PID = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {$_.MainModule.FileName -eq (Resolve-Path "main.py").Path}

# Start Vue.js app in foreground
cd ..
cd ../frontend
Start-Process -FilePath "npm" -ArgumentList "run", "serve"

# Wait for user input to kill servers
Write-Host "Press any key to stop servers"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Kill Flask server
if ($FLASK_PID) {
    Stop-Process -Id $FLASK_PID.Id
}
