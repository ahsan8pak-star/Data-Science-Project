@echo off
setlocal

set "JAVA_HOME=C:\Program Files\Java\jdk-21.0.10"

if exist "%JAVA_HOME%\bin\javac.exe" (
    "%JAVA_HOME%\bin\javac.exe" -d ..\out -sourcepath ..\src ..\src\Main.java
    echo Compilation complete. Classes in ..\out\
) else (
    echo Java compiler not found at %JAVA_HOME%
    echo Please check JAVA_HOME in this script
    pause
)

endlocal