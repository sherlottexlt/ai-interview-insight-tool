@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   InsightFlow AI - 用户访谈分析工具
echo ============================================
echo.

set "PYTHON_EXE=C:\Users\meng'yu'shao'nian\AppData\Local\Programs\Python\Python312\python.exe"

if exist "%PYTHON_EXE%" (
    echo [信息] 使用 Python 3.12
    for /f "tokens=2 delims= " %%v in ('"%PYTHON_EXE%" --version 2^>^&1') do set PYVER=%%v
    echo        版本: %PYVER%
) else (
    echo [错误] 未找到 Python 3.12
    echo        请确认安装路径正确
    pause
    exit /b 1
)

echo.
echo [启动] 正在运行 InsightFlow AI...
echo        访问地址: http://localhost:8501
echo        按 Ctrl+C 停止服务
echo.

"%PYTHON_EXE%" -m streamlit run app.py --server.port 8501 --server.headless true

pause
