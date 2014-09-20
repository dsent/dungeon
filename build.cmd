cxfreeze -OO -c --target-dir=dist src\gold_seekers.py
rmdir /S /Q dist\l10n
xcopy /E /I src\l10n dist\l10n
pause