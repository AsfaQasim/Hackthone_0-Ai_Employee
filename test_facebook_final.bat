@echo off
echo ======================================================================
echo   FACEBOOK TOKEN TEST
echo ======================================================================
echo.

python -c "import os, requests; from dotenv import load_dotenv; load_dotenv(); page_id = os.getenv('FACEBOOK_PAGE_ID'); token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'); print('Page ID:', page_id); print('Token:', token[:30] + '...'); print(); print('Testing token...'); response = requests.get(f'https://graph.facebook.com/v18.0/{page_id}', params={'fields': 'id,name', 'access_token': token}); data = response.json(); print('Result:', 'SUCCESS' if 'name' in data else 'FAILED'); print('Page Name:', data.get('name', 'N/A')) if 'name' in data else print('Error:', data.get('error', {}).get('message', 'Unknown'))"

echo.
echo ======================================================================
pause
