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

        # ✅ CORRECTED ENDPOINT BELOW
        url = "https://loginbp.ggblueshark.com/MajorModifyNickname"
        response = requests.post(url, headers=headers, data=binary_data)

        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type", "application/octet-stream")
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)