xcopy *.rtf *.html

for %%f in (*.html) do (
   rename %%f profile%%f
)