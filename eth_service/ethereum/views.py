from django.shortcuts import render
from eth_utils import to_checksum_address
from eth_hash.auto import keccak
import os
import ecdsa
from django.http import HttpResponse


def public_key_to_address(input_key):
    input_key = input_key.strip().lower().replace("0x", "")

    if not all(c in "0123456789abcdef" for c in input_key):
        raise ValueError("Input key must be in hexadecimal format.")

    if len(input_key) < 64:
        input_key = input_key.ljust(64, "0")
    elif len(input_key) > 130:
        input_key = input_key[:130]

    if len(input_key) <= 64:
        private_key_bytes = bytes.fromhex(input_key)
        public_key_bytes = private_key_to_public_key(private_key_bytes)
    else:
        public_key_bytes = bytes.fromhex(input_key)

    keccak_hash = keccak(public_key_bytes[1:])
    address = keccak_hash[-20:]
    return to_checksum_address(address)


def private_key_to_public_key(private_key):
    import ecdsa

    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return b"\x04" + vk.to_string()


def private_key_to_public_key(private_key):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return b"\x04" + vk.to_string()


def generate_private_key():
    return os.urandom(32).hex()


def download_keys(request):
    list_data = request.session.get("keys_list", [])

    content = ""
    for eth_data in list_data:
        private_key = eth_data.get("private_key", "")
        public_key = eth_data.get("public_key", "")
        eth_address = eth_data.get("eth_address", "")
        content += f"""
Private Key: {private_key}
Public Key: {public_key}
Ethereum Address: {eth_address}
\n
"""

    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=keys.txt"
    return response


def generate_keys(request):
    if "keys_list" not in request.session:
        request.session["keys_list"] = []

    context = {
        "form": None,
        "private_key": None,
        "public_key": None,
        "eth_address": None,
        "input_key": None,
        "error": None,
        "keys_list": request.session["keys_list"],
    }

    if request.method == "POST":
        if "generate_random" in request.POST:
            private_key = generate_private_key()
            private_key_bytes = bytes.fromhex(private_key)
            public_key = private_key_to_public_key(private_key_bytes).hex()
            eth_address = public_key_to_address(public_key)

            new_key_data = {
                "private_key": private_key,
                "public_key": public_key,
                "eth_address": eth_address,
            }
            print(new_key_data)

            request.session["keys_list"].append(new_key_data)
            request.session.modified = True

            context.update(new_key_data)

        elif "convert_key" in request.POST:
            input_key = request.POST.get("public_key", "")
            try:
                eth_address = public_key_to_address(input_key)
                new_key_data = {
                    "private_key": None,
                    "public_key": input_key,
                    "eth_address": eth_address,
                }
                request.session["keys_list"].append(new_key_data)
                request.session.modified = True

                context.update(new_key_data)
            except ValueError as e:
                context["error"] = str(e)

        elif "clear_keys" in request.POST:
            request.session["keys_list"] = []
            request.session.modified = True

    return render(request, "ethereum/generate_keys.html", context)
