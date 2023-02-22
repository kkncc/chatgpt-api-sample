from flask import request, jsonify
from libs.api.official import ChatBot, Prompt
from apps import app

chatBot = ChatBot()
prompt = Prompt()


@app.route('/api/chat', methods=['POST', 'GET'])
def chat():
    if request.method == "POST":
        data: dict = request.get_json()
        if not verify_data(data=data):
            return jsonify({'code': 1000, "error": "Invalid data."}), 400
        conversation_id = data.get("conversation_id", None)
        for i in range(3):
            try:
                response = chatBot.ask(
                    user_request=data["prompt"],
                    conversation_id=conversation_id
                )
                data = {
                    "code": 0,
                    "ai_text": response["choices"][0]["text"]
                }
                return jsonify(data), 200
            except Exception as exc:
                return jsonify({'code': 1001, "error": str(exc)}), 500
    else:
        data = {
            "code": 0,
        }
        return jsonify(data), 200


# 清空历史聊天记录（上下文）
@app.route('/api/reset', methods=['POST', 'GET'])
def reset():
    chatBot.reset()


def verify_data(data: dict) -> bool:
    """
    Verifies that the required fields are present in the data.
    """
    # Required fields: "prompt", "session_token"
    if "prompt" not in data:
        return False
    return True
