import webbrowser
inp = ""
webbrowser.open(''.join(chr((ord(char) - ord('a') - len(inp)) % 26 + ord('a')) if char.isalpha() else char for char in inp))