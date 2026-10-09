@echo off
setlocal

set "JAVA_HOME=C:\Program Files\Java\jdk-21.0.10"

"%~dp0gradlew.bat" test

endlocal