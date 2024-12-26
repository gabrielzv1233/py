import base64

def decode_identifier(identifier):
    main_part, shuffle_order_str = identifier.rsplit('=', 1)
    shuffle_order = [int(shuffle_order_str[i:i+2]) for i in range(0, len(shuffle_order_str), 2)]

    reversed_order = sorted(range(len(shuffle_order)), key=lambda x: shuffle_order[x])
    unshuffled = ''.join(main_part[i] for i in reversed_order)

    try:
        decoded_bytes = base64.urlsafe_b64decode(unshuffled.encode())
        decoded = decoded_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to decode Base64: {e}")

    fields = decoded.split('|')
    return fields

if __name__ == "__main__":
    identifier = input("Enter the encoded identifier: ")
    try:
        fields = decode_identifier(identifier)
        print("Decoded Fields:", fields)
    except ValueError as e:
        print(f"Error: {e}")
