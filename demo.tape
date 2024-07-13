Require issurge
Require gh

Output demo.gif

Set FontFamily "Victor Mono"
Set Theme "Catppuccin Mocha"
Set Shell "fish"
Set Width 1200
Set Height 800


Hide
Type@1ms "mkdir -p ~/.local/temp; head -n 15 exemple/exemple.issurge > ~/.local/temp/feedback" Enter
Type@1ms "cd ~/.local/temp; rm -rf playground; gh repo clone playground" Enter
Sleep 5s
Type@1ms "cd playground; mv ../feedback ./" Enter 
Ctrl+L Show


Type "head -n 10 feedback" Sleep 200ms Enter Sleep 4s

Type "issurge  feedback" Enter Sleep 20s

Type "gh issue list" Enter Sleep 5s

Hide
Type@1ms "cd ../..; rm -rf temp"
