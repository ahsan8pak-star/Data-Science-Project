@echo off
setlocal

set "JAVA_HOME=C:\Program Files\Java\jdk-21.0.10"

if exist "%JAVA_HOME%\bin\java.exe" (
    "%JAVA_HOME%\bin\java.exe" -Xshare:off -cp "..\out" Main %*
) else (
    echo Java not found at %JAVA_HOME%
    echo Please check JAVA_HOME in this script
    pause
)

endlocal