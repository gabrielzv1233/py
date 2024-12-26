import base64
import hashlib

def encode_identifier(*fields):
    combined = '|'.join(fields)
    encoded = base64.urlsafe_b64encode(combined.encode()).decode()

    shuffle_key = hashlib.sha256(combined.encode()).digest()
    shuffle_order = sorted(range(len(encoded)), key=lambda x: shuffle_key[x % len(shuffle_key)])

    shuffle_order_str = ''.join(f"{i:02d}" for i in shuffle_order[:len(encoded)])

    shuffled = ''.join(encoded[i] for i in shuffle_order)

    final_encoded = f"{shuffled}={shuffle_order_str}"
    return final_encoded

if __name__ == "__main__":
    encoded = encode_identifier(input("Artist Name: "), input("Album Name: "), input("Song Name: "))
    print("Encoded Identifier:", encoded)
