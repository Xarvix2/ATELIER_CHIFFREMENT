import os
from cryptography.fernet import Fernet
from pathlib import Path
import argparse

def load_key() -> bytes:
    key = os.environ.get("FERNET_KEY")
    if not key:
        raise SystemExit("❌ Secret GitHub FERNET_KEY non défini dans l'environnement.")
    return key.encode()

def encrypt_file(input_path: Path, output_path: Path):
    f = Fernet(load_key())
    data = input_path.read_bytes()
    token = f.encrypt(data)
    output_path.write_bytes(token)

def decrypt_file(input_path: Path, output_path: Path):
    f = Fernet(load_key())
    token = input_path.read_bytes()
    data = f.decrypt(token)
    output_path.write_bytes(data)

def main():
    parser = argparse.ArgumentParser(description="Atelier 1 : Fernet avec Secret GitHub")
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if args.mode == "encrypt":
        encrypt_file(in_path, out_path)
        print("🔐 Fichier chiffré avec Fernet (clé GitHub Secret).")
    else:
        decrypt_file(in_path, out_path)
        print("🔓 Fichier déchiffré avec Fernet (clé GitHub Secret).")

if __name__ == "__main__":
    main()
