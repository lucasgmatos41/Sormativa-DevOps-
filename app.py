from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# armazenamento simples em memória
todos = {}
next_id = 1

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/todos", methods=["GET"])
def list_todos():
    return jsonify(list(todos.values()))

@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title é obrigatório"}), 400
    todo = {
        "id": next_id,
        "title": data["title"],
        "completed": bool(data.get("completed", False))
    }
    todos[next_id] = todo
    next_id += 1
    return jsonify(todo), 201

@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify(todo)

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    todo["title"] = data.get("title", todo["title"])
    todo["completed"] = bool(data.get("completed", todo["completed"]))
    return jsonify(todo)

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    if todo_id not in todos:
        abort(404)
    del todos[todo_id]
    return "", 204
