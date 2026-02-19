@echo off
chcp 65001 >nul
title 农村三资数据大屏
echo ========================================
echo   农村集体经济组织三资公示数字大屏
echo ========================================
echo.
echo Starting server...
python "%~dp0start.py"
pause
