from Crypto.Cipher import AES from Crypto.Util.Padding import pad import binascii from flask import Flask, request, jsonify import requests import uid_generator_pb2 from a_pb2 import CSGetPlayerPersonalShowRes from secret import key, iv

app = Flask(name)

def hex_to_bytes(hex_string): return bytes.fromhex(hex_string)

def create_protobuf(akiru_, aditya): message = uid_generator_pb2.uid_generator() message.akiru_ = akiru_ message.aditya = aditya return message.SerializeToString()

def protobuf_to_hex(protobuf_data): return binascii.hexlify(protobuf_data).decode()

def decode_hex(hex_string): byte_data = binascii.unhexlify(hex_string.replace(' ', '')) users = CSGetPlayerPersonalShowRes() users.ParseFromString(byte_data) return users

def encrypt_aes(hex_data, key, iv): key = key.encode()[:16] iv = iv.encode()[:16] cipher = AES.new(key, AES.MODE_CBC, iv) padded_data = pad(bytes.fromhex(hex_data), AES.block_size) encrypted_data = cipher.encrypt(padded_data) return binascii.hexlify(encrypted_data).decode()

def get_credentials(region): region = region.upper() if region == "IND": return "3942040791", "EDD92B8948F4453F544C9432DFB4996D02B4054379A0EE083D8459737C50800B" return "uid", "password"

def get_jwt_token(region): uid, password = get_credentials(region) jwt_url = f"https://jwt-aditya.vercel.app/token?uid={uid}&password={password}" response = requests.get(jwt_url) if response.status_code != 200: return None return response.json()

@app.route('/player-info', methods=['GET']) def main(): uid = request.args.get('uid') region = request.args.get('region')

if not uid or not region:
    return jsonify({"error": "Missing 'uid' or 'region' query parameter"}), 400

try:
    saturn_ = int(uid)
except ValueError:
    return jsonify({"error": "Invalid UID"}), 400

jwt_info = get_jwt_token(region)
if not jwt_info or 'token' not in jwt_info:
    return jsonify({"error": "Failed to fetch JWT token"}), 500

api = jwt_info['serverUrl']
token = jwt_info['token']

protobuf_data = create_protobuf(saturn_, 1)
hex_data = protobuf_to_hex(protobuf_data)
encrypted_hex = encrypt_aes(hex_data, key, iv)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Dalvik/2.1.0 (Linux; Android 9)',
    'X-Unity-Version': '2018.4.11f1'
}

try:
    response = requests.post(f"{api}/GetPlayerPersonalShow", headers=headers, data=bytes.fromhex(encrypted_hex))
    response.raise_for_status()
except requests.RequestException:
    return jsonify({"error": "Failed to contact game server"}), 502

hex_response = response.content.hex()

try:
    users = decode_hex(hex_response)
except Exception as e:
    return jsonify({"error": f"Failed to parse Protobuf: {str(e)}"}), 500

result = {}

if users.players:
    result['account_basic_info'] = []
    for p in users.players:
        result['account_basic_info'].append({
            'user_id': p.user_id,
            'username': p.username,
            'level': p.level,
            'rank': p.rank,
            'last_login': p.last_login,
            'country_code': p.country_code,
            'avatar': p.avatar,
            'banner': p.banner,
            'game_version': p.game_version,
            'is_online': p.is_online,
            'in_match': p.in_match
        })
        if p.HasField("clan_tag"):
            result['clan_tag'] = {
                'tag_display': p.clan_tag.tag_display,
                'unknown_field_7': p.clan_tag.unknown_field_7
            }
        if p.HasField("premium"):
            result['premium_info'] = {
                'premium_level': p.premium.premium_level,
                'premium_days': p.premium.premium_days
            }

if users.HasField("clan"):
    result['guild_info'] = {
        'clan_name': users.clan.clan_name,
        'clan_level': users.clan.clan_level,
        'clan_xp': users.clan.clan_xp,
        'clan_xp_required': users.clan.clan_xp_required
    }

if users.HasField("inventory"):
    result['inventory_details'] = {
        'inventory_id': users.inventory.inventory_id,
        'capacity': users.inventory.capacity,
        'version': users.inventory.version,
        'is_equipped': users.inventory.is_equipped,
        'last_update': users.inventory.last_update,
        'item_count': len(users.inventory.items)
    }

if users.HasField("achievement"):
    result['achievements'] = {
        'achievement_id': users.achievement.achievement_id,
        'progress': users.achievement.progress,
        'current_level': users.achievement.current_level
    }

if users.HasField("currency"):
    result['currency'] = {
        'coins': users.currency.coins
    }

result['credit'] = '@Ujjaiwal'
result['profile_url'] = f"https://freefire-profile.vercel.app/player?uid={uid}&region={region}"

return jsonify(result)

if name == "main": app.run(host="0.0.0.0", port=5000)

