Output artifacts/local-setup.gif

Set Shell powershell
Set Width 1400
Set Height 780
Set FontSize 18
Set Framerate 30
Set PlaybackSpeed 1.0
Set Theme "Dracula"
Set Padding 18
Set WindowBar Colorful
Set WaitTimeout 20s

Require python
Require npm
Require docker

Type "cd C:\Users\shail\source\AlphaQuant\frontend"
Enter
Sleep 1s

Type "npm install"
Enter
Sleep 4s

Type "npm run dev -- --host 127.0.0.1 --port 5173"
Enter
Sleep 4s

Type "echo Local UI dev server is ready"
Enter
Sleep 2s
