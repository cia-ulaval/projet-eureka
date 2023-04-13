#!/bin/bash

# Start Flask server in background
cd backend || exit
flask run &
FLASK_PID=$!

# Start Vue.js app in foreground
cd ../frontend || exit
npm run serve &
VUE_PID=$!

# Wait for user input to kill servers
echo "Press any key to stop servers"
read -n 1 -s

# Kill Flask server
kill $FLASK_PID

# Kill Vue.js app
kill $VUE_PID
