from flask import Flask, request, jsonify, Response
import requests
import modify_nickname_pb2  # Make sure this is generated via protoc

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Use /change_name?token=xxx&nickname=xxx"
    })

@app.route("/change_name", methods=["GET"])
def change_name():
    try:
        jwt_token = request.args.get("token")
        nickname = request.args.get("nickname")

        if not jwt_token or not nickname:
            return jsonify({"status": "error", "message": "Missing 'token' or 'nickname'"}), 400

        # Build the Protobuf request
        req = modify_nickname_pb2.ModifyNicknameReq()
        req.nickname = nickname
        req.account_id = 0  # Can update if needed

        binary_data = req.SerializeToString()

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/x-protobuf",
            "User-Agent": "Dalvik/2.1.0 (Linux; Android 10)",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": "OB50"
        }

        url = "https://loginbp.ggblueshark.com/MajorModifyNickname"
        response = requests.post(url, headers=headers, data=binary_data)

        # HTTP status code के आधार पर check करें
        if response.status_code == 200:
            # Successful response (200 OK)
            # Response content की length check करें (empty response often indicates success)
            if len(response.content) == 0:
                return jsonify({
                    "status": "success", 
                    "message": "Nickname changed successfully",
                    "new_nickname": nickname
                })
            else:
                # Non-empty response - might contain error information
                try:
                    # Try to decode as text to see if there's a readable error message
                    error_message = response.content.decode('utf-8', errors='ignore')
                    return jsonify({
                        "status": "error", 
                        "message": f"Server returned non-empty response: {error_message}"
                    }), 400
                except:
                    return jsonify({
                        "status": "error", 
                        "message": "Server returned non-empty binary response (might be protobuf)"
                    }), 400
        else:
            # Error status code
            return jsonify({
                "status": "error", 
                "message": f"Server returned error status: {response.status_code}",
                "response_content": response.content.decode('utf-8', errors='ignore') if response.content else None
            }), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)