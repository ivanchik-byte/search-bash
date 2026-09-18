# Output destination
Output demo.gif

# Visual styling
Set Shell "bash"
Set FontSize 18
Set FontFamily "JetBrains Mono"
Set Width 900
Set Height 520
Set Padding 20
Set BorderRadius 10
Set WindowBar Colorful
Set WindowBarSize 40
Set Theme "Catppuccin Mocha"
Set TypingSpeed 45ms

# Hide environment setup
Hide
Type "export PATH=$PWD:$PATH"
Enter
Type "clear"
Enter
Show

# Step 1: Technical lookup with live search
Sleep 500ms
Type "search 'how to configure nginx websocket reverse proxy'"
Sleep 400ms
Enter
Sleep 4s

# Step 2: Clear screen for command generation
Type "clear"
Enter
Sleep 500ms

# Step 3: Shell command generator
Type "search -c 'find all files over 500MB modified in the last 7 days'"
Sleep 400ms
Enter
Sleep 3.5s
Type "n"
Sleep 300ms
Enter
Sleep 2s
