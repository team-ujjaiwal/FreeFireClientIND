from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from flask import Flask, request, jsonify
import requests
import uid_generator_pb2
from a_pb2 import CSGetPlayerPersonalShowRes
from secret import key, iv

app = Flask(__name__)

# Helper: Convert proto to dict (recursively)
def proto_to_dict(message):
    result = {}
    for field, value in message.ListFields():
        if field.label == field.LABEL_REPEATED:
            result[field.name] = [proto_to_dict(v) if hasattr(v, 'ListFields') else v for v in value]
        else:
            result[field.name] = proto_to_dict(value) if hasattr(value, 'ListFields') else value
    return result

# Convert proto to bytes
def create_protobuf(akiru_, aditya):
    message = uid_generator_pb2.uid_generator()
    message.akiru_ = akiru_
    message.aditya = aditya
    return message.SerializeToString()

# Encrypt protobuf bytes using AES
def encrypt_aes(data_bytes, key, iv):
    key_bytes = key.encode()[:16]
    iv_bytes = iv.encode()[:16]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    padded_data = pad(data_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted

# Decode response protobuf hex to object
def decode_response(hex_string):
    byte_data = binascii.unhexlify(hex_string)
    message = CSGetPlayerPersonalShowRes()
    message.ParseFromString(byte_data)
    return message

# UID-password for JWT
def get_credentials(region):
    region = region.upper()
    if region == "IND":
        return "3942040791", "EDD92B8948F4453F544C9432DFB4996D02B4054379A0EE083D8459737C50800B"
    return "uid", "password"

# JWT token fetch
def get_jwt_token(region):
    uid, password = get_credentials(region)
    url = f"https://jwt-aditya.vercel.app/token?uid={uid}&password={password}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None

@app.route("/player-info", methods=["GET"])
def player_info():
    uid = request.args.get("uid")
    region = request.args.get("region", "IND")

    if not uid or not region:
        return jsonify({"error": "Missing UID or region"}), 400

    try:
        uid_int = int(uid)
    except ValueError:
        return jsonify({"error": "Invalid UID"}), 400

    # Step 1: Get JWT + server URL
    jwt_data = get_jwt_token(region)
    if not jwt_data or "token" not in jwt_data:
        return jsonify({"error": "JWT token fetch failed"}), 500

    server_url = jwt_data["serverUrl"]
    token = jwt_data["token"]

    # Step 2: Create UID proto → encrypt
    proto_bytes = create_protobuf(uid_int, 1)
    encrypted_body = encrypt_aes(proto_bytes, key, iv)

    # Step 3: Send POST request to Free Fire endpoint
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Dalvik/2.1.0",
        "X-Unity-Version": "2018.4.11f1",
        "ReleaseVersion": "OB49",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        res = requests.post(
            url=f"{server_url}/GetPlayerPersonalShow",
            headers=headers,
            data=encrypted_body
        )
        res.raise_for_status()
    except Exception as e:
        return jsonify({"error": "Game server request failed", "details": str(e)}), 502

    # Step 4: Decode Proto response
    try:
        proto_message = decode_response(res.content.hex())
        result_json = proto_to_dict(proto_message)
        result_json["credit"] = "@Ujjaiwal"
        return jsonify(result_json)
    except Exception as e:
        return jsonify({"error": "Failed to parse proto", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)