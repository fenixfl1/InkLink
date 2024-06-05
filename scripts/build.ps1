# use pyinstaller to create an executable
pyinstaller --name InkLInk --onefile --add-data config.ini:config.ini --hidden-import=win32timezone manage.py