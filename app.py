from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from flask import Flask, request, jsonify
import requests
import random
import uid_generator_pb2
from a_pb2 import CSGetPlayerPersonalShowRes
from secret import key, iv

app = Flask(__name__)

def hex_to_bytes(hex_string):
    return bytes.fromhex(hex_string)

def create_protobuf(akiru_, aditya):
    message = uid_generator_pb2.uid_generator()
    message.akiru_ = akiru_
    message.aditya = aditya
    return message.SerializeToString()

def protobuf_to_hex(protobuf_data):
    return binascii.hexlify(protobuf_data).decode()

def decode_hex(hex_string):
    byte_data = binascii.unhexlify(hex_string.replace(' ', ''))
    users = CSGetPlayerPersonalShowRes()
    users.ParseFromString(byte_data)
    return users

def encrypt_aes(hex_data, key, iv):
    key = key.encode()[:16]
    iv = iv.encode()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(bytes.fromhex(hex_data), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return binascii.hexlify(encrypted_data).decode()

def get_credentials(region):
    region = region.upper()
    if region == "IND":
        return "3942040791", "EDD92B8948F4453F544C9432DFB4996D02B4054379A0EE083D8459737C50800B"
    elif region in ["NA", "BR", "SAC", "US"]:
        return "uid", "password"
    else:
        return "uid", "password"

def get_jwt_token(region):
    uid, password = get_credentials(region)
    jwt_url = f"https://jwt-aditya.vercel.app/token?uid={uid}&password={password}"
    response = requests.get(jwt_url)
    if response.status_code != 200:
        return None
    return response.json()

@app.route('/player-info', methods=['GET'])
def main():
    uid = request.args.get('uid')
    region = request.args.get('region')

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
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
        'Connection': 'Keep-Alive',
        'Expect': '100-continue',
        'Authorization': f'Bearer {token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB49',
        'Content-Type': 'application/x-www-form-urlencoded',
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
        result['players'] = []
        for p in users.players:
            player_data = {
                'user_id': p.user_id,
                'account_type': p.account_type,
                'username': p.username,
                'country_code': p.country_code,
                'age': p.age,
                'level': p.level,
                'banner': p.banner,
                'avatar': p.avatar,
                'rank': p.rank,
                'experience_points': p.experience_points,
                'unknown_field_17': p.unknown_field_17,
                'matches_played': p.matches_played,
                'unique_identifier': p.unique_identifier,
                'combat_skill': p.combat_skill,
                'total_kills': p.total_kills,
                'last_login': p.last_login,
                'health': p.health,
                'stamina': p.stamina,
                'encrypted_data': p.encrypted_data.hex() if p.encrypted_data else None,
                'current_rank': p.current_rank,
                'max_health': p.max_health,
                'clan_join_date': p.clan_join_date,
                'unknown_field_48': p.unknown_field_48,
                'game_version': p.game_version,
                'is_online': p.is_online,
                'in_match': p.in_match
            }
            
            # Clan tag information
            if p.HasField("clan_tag"):
                player_data['clan_tag'] = {
                    'tag_bytes': p.clan_tag.tag_bytes.hex() if p.clan_tag.tag_bytes else None,
                    'tag_display': p.clan_tag.tag_display,
                    'unknown_field_7': p.clan_tag.unknown_field_7
                }
            
            # Premium features
            if p.HasField("premium"):
                player_data['premium'] = {
                    'premium_level': p.premium.premium_level,
                    'premium_days': p.premium.premium_days
                }
            
            # Stats
            if p.stats:
                player_data['stats'] = []
                for stat in p.stats:
                    stat_data = {
                        'stat_id': stat.stat_id,
                        'tier': stat.tier,
                        'details': {
                            'stat_type': stat.details.stat_type,
                            'progress': stat.details.progress,
                            'max_value': stat.details.max_value,
                            'unlocks': stat.details.unlocks,
                            'completed': stat.details.completed
                        } if stat.HasField("details") else None
                    }
                    player_data['stats'].append(stat_data)
            
            # Recent activity
            if p.HasField("activity"):
                player_data['activity'] = []
                for entry in p.activity.entries:
                    player_data['activity'].append({
                        'activity_type': entry.activity_type,
                        'timestamp': entry.timestamp,
                        'count': entry.count
                    })
            
            # Status indicator
            if p.HasField("status_indicator"):
                player_data['status_indicator'] = {
                    'status_type': p.status_indicator.status_type,
                    'status_value': p.status_indicator.status_value
                }
            
            result['players'].append(player_data)

    # Clan information
    if users.HasField("clan"):
        result["clan"] = {
            "member_id_1": users.clan.member_id_1,
            "clan_name": users.clan.clan_name,
            "member_id_2": users.clan.member_id_2,
            "clan_level": users.clan.clan_level,
            "clan_xp": users.clan.clan_xp,
            "clan_xp_required": users.clan.clan_xp_required
        }

    # Inventory information
    if users.HasField("inventory"):
        inventory_data = {
            "inventory_id": users.inventory.inventory_id,
            "capacity": users.inventory.capacity,
            "inventory_hash": users.inventory.inventory_hash.hex() if users.inventory.inventory_hash else None,
            "version": users.inventory.version,
            "is_equipped": users.inventory.is_equipped,
            "last_update": users.inventory.last_update,
            "unknown_field_12": users.inventory.unknown_field_12,
            "items": []
        }
        
        for item in users.inventory.items:
            item_data = {
                "quantity": item.quantity
            }
            if item.HasField("consumable"):
                item_data["type"] = "consumable"
                item_data["id"] = item.consumable
            elif item.HasField("weapon"):
                item_data["type"] = "weapon"
                item_data["id"] = item.weapon
            elif item.HasField("skin"):
                item_data["type"] = "skin"
                item_data["id"] = item.skin
            
            inventory_data["items"].append(item_data)
        
        result["inventory"] = inventory_data

    # Teammate information
    if users.HasField("teammate"):
        teammate = users.teammate
        result["teammate"] = {
            "user_id": teammate.user_id,
            "username": teammate.username,
            "level": teammate.level,
            "rank": teammate.rank,
            "is_online": teammate.is_online
        }

    # Achievement information
    if users.HasField("achievement"):
        result["achievement"] = {
            "achievement_id": users.achievement.achievement_id,
            "progress": users.achievement.progress,
            "current_level": users.achievement.current_level,
            "reward_id": users.achievement.reward_id,
            "target_id": users.achievement.target_id,
            "unlock_tier": users.achievement.unlock_tier
        }

    # Player status
    if users.HasField("status"):
        result["status"] = {
            "status_id": users.status.status_id,
            "unknown_field_2": users.status.unknown_field_2,
            "status_level": users.status.status_level,
            "status_message": users.status.status_message,
            "status_flags": users.status.status_flags,
            "custom_data": users.status.custom_data.hex() if users.status.custom_data else None
        }

    # Currency
    if users.HasField("currency"):
        result["currency"] = {
            "coins": users.currency.coins
        }

    # Time limited event
    if users.HasField("event"):
        result["event"] = {
            "event_id": users.event.event_id,
            "unknown_field_3": users.event.unknown_field_3,
            "start_time": users.event.start_time,
            "end_time": users.event.end_time,
            "is_active": users.event.is_active
        }

    result['credit'] = '@Ujjaiwal'
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)