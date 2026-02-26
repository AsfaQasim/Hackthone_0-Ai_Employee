@echo off
echo ============================================
echo WhatsApp Access Token - Quick Guide
echo ============================================
echo.
echo STEP 1: Open Meta Developers
echo ============================================
echo.
echo Opening browser...
start https://developers.facebook.com/
echo.
echo ✓ Browser opened!
echo.
echo ============================================
echo STEP 2: Follow These Steps
echo ============================================
echo.
echo 1. Login with Facebook account
echo 2. Click "My Apps" (top right)
echo 3. Click "Create App"
echo 4. Select "Business" type
echo 5. Fill app name: "My WhatsApp Bot"
echo 6. Click "Create App"
echo.
echo ============================================
echo STEP 3: Add WhatsApp Product
echo ============================================
echo.
echo 1. In app dashboard, find "Add Product"
echo 2. Find "WhatsApp"
echo 3. Click "Set Up"
echo.
echo ============================================
echo STEP 4: Get Access Token
echo ============================================
echo.
echo 1. Go to: WhatsApp ^> Getting Started
echo 2. Scroll down
echo 3. Find "Temporary access token"
echo 4. Click "Copy" button
echo.
echo Token looks like:
echo EAABsbCS1iHgBO4rqDwFZC8ZAn7ZBqBAZC...
echo.
echo ============================================
echo STEP 5: Get Phone Number ID
echo ============================================
echo.
echo On same page:
echo 1. Find "Phone number ID"
echo 2. Copy the number
echo.
echo Looks like: 123456789012345
echo.
echo ============================================
echo STEP 6: Configure .env File
echo ============================================
echo.
echo Create .env file with:
echo.
echo WHATSAPP_PHONE_ID=your_phone_id
echo WHATSAPP_ACCESS_TOKEN=your_token
echo.
echo ============================================
echo STEP 7: Test
echo ============================================
echo.
echo Run: python whatsapp_business_api.py check
echo.
echo ============================================
echo.
pause
