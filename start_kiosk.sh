#!/bin/bash

# Raspberry Pi 4 Kiosk Mode Script for Recode Application
# With touch screen support

# Configuration
FLASK_APP_PATH="/home/boog/Desktop/Llama-Recoil"
FLASK_PORT=5000
DISPLAY_URL="http://127.0.0.1:${FLASK_PORT}"

# Set display for X server
export DISPLAY=:0

# Change to app directory
cd "$FLASK_APP_PATH" || exit 1

# Disable screen blanking and power saving
xset s off 2>/dev/null
xset s noblank 2>/dev/null
xset -dpms 2>/dev/null

# Hide mouse cursor after 0.5 seconds of inactivity (for touch screen)
unclutter -idle 0.5 -root &

# Wait for X server to be ready
sleep 2

# Start the Flask application in the background
source venv/bin/activate
python main.py &
FLASK_PID=$!

# Wait for Flask server to start
echo "Waiting for Flask server to start..."
sleep 5

# Launch Chromium in kiosk mode with touch screen support
chromium \
    --kiosk \
    --noerrdialogs \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --disable-restore-session-state \
    --disable-component-update \
    --check-for-update-interval=31536000 \
    --disable-pinch \
    --overscroll-history-navigation=0 \
    --touch-events=enabled \
    --enable-touch-drag-drop \
    --enable-touchview \
    --disable-translate \
    --disable-features=TranslateUI \
    --no-first-run \
    --fast \
    --fast-start \
    --disable-background-networking \
    --disable-sync \
    --disable-default-apps \
    --disable-extensions \
    --disable-hang-monitor \
    --disable-popup-blocking \
    --disable-prompt-on-repost \
    --ignore-certificate-errors \
    --allow-running-insecure-content \
    "$DISPLAY_URL"

# When Chromium closes, kill the Flask server
kill $FLASK_PID 2>/dev/null
