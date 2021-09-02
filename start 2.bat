@echo off
chcp 65001
:: Ввод данных:
set /p Data="твой ник в майнкрафте: "
 
:: "Идентификация" данных:
echo %Data%>nick
 
pause>nul