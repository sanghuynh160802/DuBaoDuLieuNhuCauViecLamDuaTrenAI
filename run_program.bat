@echo off
echo ================================
echo 🚀 RUNNING ALL JOBINFOR SERVICES
echo ================================

:: Start NodeJS Backend
echo 🔄 Starting NodeJS Backend...
start "NodeJS Backend" cmd /k ^
cd /d "D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\QLVLBackEnd" ^&^& npm start

:: Start Python API
echo 🔄 Starting Python Forecast API...
start "Python API" cmd /k ^
cd /d "D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI" ^&^& call venv\Scripts\activate ^&^& python -u server.py

:: Start VueJS Frontend
echo 🔄 Starting VueJS Frontend...
start "VueJS Frontend" cmd /k ^
cd /d "D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\QLVLFrontEnd" ^&^& npm run dev

echo ✅ All services started in separate terminals.
pause
