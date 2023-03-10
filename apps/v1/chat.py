from flask import request, jsonify
from libs.api.turbo import ChatBot
from libs.api.image import ImageBot
from apps import app

chatBot = ChatBot()
imageBot = ImageBot()


@app.route('/api/chat', methods=['POST', 'GET'])
def chat():
    if request.method == "POST":
        data: dict = request.get_json()
        if not verify_data(data=data):
            return jsonify({'code': 1000, "error": "Invalid data."}), 400
        conversation_id = data.get("conversation_id", None)
        is_image = data.get("image", "")
        status_code = 200
        for _ in range(3):
            try:
                if is_image == "Y" or "#picture" in data["prompt"]:
                    response = imageBot.ask(
                        user_request=data["prompt"],
                        conversation_id=conversation_id
                    )
                    data = {
                        "code": 0,
                        "ai_url": response["data"][0]["url"]
                    }
                else:
                    response = chatBot.ask(
                        user_request=data["prompt"],
                        conversation_id=conversation_id
                    )
                    data = {
                        "code": 0,
                        "ai_text": response["choices"][0]["message"]["content"]
                    }
                break
            except Exception as exc:
                data = {
                    'code': 1001,
                    "error": str(exc)
                }
                status_code = 500
        return jsonify(data), status_code
    else:
        data = {
            "code": 0,
        }
        return jsonify(data), 200


# 清空历史聊天记录（上下文）
@app.route('/api/reset', methods=['POST', 'GET'])
def reset():
    chatBot.reset()
    data = {
        "code": 0,
    }
    return jsonify(data), 200


def verify_data(data: dict) -> bool:
    """
    Verifies that the required fields are present in the data.
    """
    # Required fields: "prompt", "session_token"
    if "prompt" not in data:
        return False
    return True
