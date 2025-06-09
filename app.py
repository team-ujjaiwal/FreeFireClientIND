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
        response = requests.post(f"{serverUrl}/GetPlayerPersonalShow", headers=headers, data=bytes.fromhex(encrypted_hex))
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
                'account_status': p.account_status,
                'username': p.username,
                'country_code': p.country_code,
                'level': p.level,
                'experience': p.experience,
                'clan_id': p.clan_id,
                'title_id': p.title_id,
                'matches_played': p.matches_played,
                'kills': p.kills,
                'daily_challenges': p.daily_challenges,
                'current_avatar': p.current_avatar,
                'main_weapon': p.main_weapon,
                'cosmetic_skin': p.cosmetic_skin,
                'last_login': p.last_login,
                'rank': p.rank,
                'skill_rating': p.skill_rating,
                'headshot_percentage': p.headshot_percentage,
                'current_rank': p.current_rank,
                'clan_tag': p.clan_tag,
                'join_date': p.join_date,
                'game_version': p.game_version,
                'email_verified': p.email_verified,
                'phone_verified': p.phone_verified,
                'is_online': p.is_online,
                'in_match': p.in_match
            }
            
            # Add subscription info if available
            if p.HasField("subscription"):
                player_data['subscription'] = {
                    'tier': p.subscription.tier,
                    'renewal_period': p.subscription.renewal_period
                }
                
            # Add equipped items if available
            if p.HasField("equipped"):
                equipped_items = []
                for slot in p.equipped.slots:
                    equipped_items.append({
                        'slot_type': slot.slot_type,
                        'item_id': slot.item_id,
                        'variant': slot.variant
                    })
                player_data['equipped_items'] = equipped_items
                
            # Add region info if available
            if p.HasField("region"):
                player_data['region_info'] = {
                    'region_id': p.region.region_id,
                    'ping': p.region.ping
                }
                
            # Add achievements if available
            if p.achievements:
                achievements = []
                for achievement in p.achievements:
                    ach_data = {
                        'achievement_id': achievement.achievement_id,
                        'progress': achievement.progress
                    }
                    if achievement.HasField("details"):
                        ach_data['details'] = {
                            'objective_type': achievement.details.objective_type,
                            'target_value': achievement.details.target_value,
                            'current_value': achievement.details.current_value,
                            'reward_type': achievement.details.reward_type,
                            'reward_amount': achievement.details.reward_amount
                        }
                    achievements.append(ach_data)
                player_data['achievements'] = achievements
                
            result['players'].append(player_data)

    if users.clans:
        result['clans'] = []
        for clan in users.clans:
            clan_data = {
                'clan_id': clan.clan_id,
                'member_count': clan.member_count,
                'status': clan.status,
                'permission_level': clan.permission_level,
                'creation_date': clan.creation_date
            }
            
            # Add clan ranks if available
            if clan.ranks:
                ranks = []
                for rank in clan.ranks:
                    rank_data = {}
                    if rank.HasField("custom_rank"):
                        rank_data['custom_rank'] = rank.custom_rank
                    if rank.HasField("standard_rank"):
                        rank_data['standard_rank'] = rank.standard_rank
                    ranks.append(rank_data)
                clan_data['ranks'] = ranks
                
            result['clans'].append(clan_data)

    if users.titles:
        result['titles'] = []
        for title in users.titles:
            result['titles'].append({
                'title_id': title.title_id,
                'title_name': title.title_name,
                'unlock_requirement': title.unlock_requirement,
                'rarity': title.rarity,
                'usage_count': title.usage_count,
                'category': title.category
            })

    if users.HasField("detailed_player"):
        result['detailed_player'] = {
            'user_id': users.detailed_player.user_id,
            'username': users.detailed_player.username,
            'level': users.detailed_player.level
            # Add more fields as needed
        }

    if users.HasField("social"):
        result['social'] = {
            'friends_count': users.social.friends_count,
            'friend_requests': users.social.friend_requests,
            'max_friends': users.social.max_friends,
            'blocked_count': users.social.blocked_count,
            'favorite_friend': users.social.favorite_friend,
            'preferred_region': users.social.preferred_region
        }

    if users.HasField("profile"):
        result['profile_customization'] = {
            'user_id': users.profile.user_id,
            'banner': users.profile.banner,
            'bio': users.profile.bio,
            'layout_style': users.profile.layout_style,
            'custom_url': users.profile.custom_url
        }

    if users.HasField("settings"):
        result['settings'] = {
            'sensitivity': users.settings.sensitivity
        }

    if users.HasField("session"):
        result['session'] = {
            'current_streak': users.session.current_streak,
            'session_start': users.session.session_start,
            'session_end': users.session.session_end,
            'match_count': users.session.match_count
        }

    if users.unlocks:
        result['unlocks'] = []
        for unlock in users.unlocks:
            result['unlocks'].append({
                'item_id': unlock.item_id,
                'unlock_type': unlock.unlock_type
            })

    if users.currencies:
        result['currencies'] = []
        for currency in users.currencies:
            result['currencies'].append({
                'currency_type': currency.currency_type,
                'amount': currency.amount,
                'max_capacity': currency.max_capacity,
                'bonus': currency.bonus
            })

    if users.HasField("inventory"):
        result["inventory"] = {
            "inventory_id": users.inventory.inventory_id,
            "capacity": users.inventory.capacity,
            "version": users.inventory.version,
            "is_equipped": users.inventory.is_equipped,
            "last_update": users.inventory.last_update,
            "item_count": len(users.inventory.items)
        }

    result['credit'] = '@Ujjaiwal'
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)