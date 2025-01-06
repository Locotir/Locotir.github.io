from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Obtener los secretos desde las variables de entorno
token = os.getenv('TOKEN')
gist_id = os.getenv('GIST_ID')

if not token or not gist_id:
    raise ValueError("TOKEN or GIST_ID is not set")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Función para leer el contenido del gist
def read_gist():
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Función para escribir contenido en el gist
def write_gist(content):
    data = {
        "files": {
            "hash2ip.txt": {
                "content": content
            }
        }
    }
    response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)
    return response.status_code == 200

@app.route('/read', methods=['GET'])
def read():
    hash_value = request.args.get('hash')
    gist_content = read_gist()
    if gist_content and "hash2ip.txt" in gist_content["files"]:
        file_content = gist_content["files"]["hash2ip.txt"]["content"]
        lines = file_content.splitlines()
        for line in lines:
            if line.startswith(hash_value):
                return jsonify({"content": line})
        return jsonify({"error": f"Hash {hash_value} not found"}), 404
    else:
        return jsonify({"error": "hash2ip.txt not found"}), 404

@app.route('/modify', methods=['POST'])
def modify():
    hash_value = request.json.get('hash')
    new_ip = request.json.get('ip')
    gist_content = read_gist()
    if gist_content and "hash2ip.txt" in gist_content["files"]:
        file_content = gist_content["files"]["hash2ip.txt"]["content"]
        lines = file_content.splitlines()
        updated_lines = []
        found = False
        for line in lines:
            if line.startswith(hash_value):
                updated_lines.append(f"{hash_value},{new_ip}")
                found = True
            else:
                updated_lines.append(line)
        if not found:
            return jsonify({"error": f"Hash {hash_value} not found"}), 404
        updated_content = "\n".join(updated_lines)
        success = write_gist(updated_content)
        if success:
            return jsonify({"message": "Content updated successfully"})
        else:
            return jsonify({"error": "Failed to update content"}), 500
    else:
        return jsonify({"error": "hash2ip.txt not found"}), 404

@app.route('/add', methods=['POST'])
def add():
    hash_value = request.json.get('hash')
    ip_value = request.json.get('ip')
    gist_content = read_gist()
    if gist_content and "hash2ip.txt" in gist_content["files"]:
        file_content = gist_content["files"]["hash2ip.txt"]["content"]
        new_line = f"{hash_value},{ip_value}"
        if any(line.startswith(hash_value) for line in file_content.splitlines()):
            return jsonify({"error": f"Hash {hash_value} already exists"}), 409
        updated_content = file_content + "\n" + new_line
        success = write_gist(updated_content)
        if success:
            return jsonify({"message": "Content added successfully"})
        else:
            return jsonify({"error": "Failed to add content"}), 500
    else:
        return jsonify({"error": "hash2ip.txt not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
