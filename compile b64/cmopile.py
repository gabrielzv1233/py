import base64

compile_file = './AAAAA.mp3'

with open(compile_file, 'rb') as file:
    mp3_data = file.read()

mp3_base64 = base64.b64encode(mp3_data).decode('utf-8')

with open('compile b64/output.txt', 'w') as file:
    file.write(mp3_base64)
