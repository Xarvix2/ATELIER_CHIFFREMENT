import argparse
import os
from pathlib import Path
from nacl.secret import SecretBox
from nacl.utils import random
import base64

def load_key() -> bytes:
    key = os.environ.get("SECRETBOX_KEY")
    if not key:
        raise SystemExit("❌ SECRETBOX_KEY non défini dans l'environnement.")
    return base64.b64decode(key)

def encrypt_file(input_path: Path, output_path: Path):
    key = load_key()
    box = SecretBox(key)

    data = input_path.read_bytes()
    nonce = random(SecretBox.NONCE_SIZE)
    encrypted = box.encrypt(data, nonce)

    output_path.write_bytes(encrypted)

def decrypt_file(input_path: Path, output_path: Path):
    key = load_key()
    box = SecretBox(key)

    encrypted = input_path.read_bytes()
    data = box.decrypt(encrypted)

    output_path.write_bytes(data)

def main():
    parser = argparse.ArgumentParser(description="Atelier 2 : SecretBox (PyNaCl)")
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if args.mode == "encrypt":
        encrypt_file(in_path, out_path)
        print("🔐 Fichier chiffré avec SecretBox.")
    else:
        decrypt_file(in_path, out_path)
        print("🔓 Fichier déchiffré avec SecretBox.")

if __name__ == "__main__":
    main()
