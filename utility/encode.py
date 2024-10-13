input_text = input("Text to encode:\n>> ")
encoded_text = ''.join(chr((ord(char) - ord('a') + len(input_text)) % 26 + ord('a')) if char.isalpha() else char for char in input_text)
print(encoded_text)