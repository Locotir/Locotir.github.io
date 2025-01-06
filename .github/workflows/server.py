import os
import sys
import requests

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

# Procesar los argumentos
action = sys.argv[1]
hash_value = sys.argv[2] if len(sys.argv) > 2 else None
ip_value = sys.argv[3] if len(sys.argv) > 3 else None

result = ""

if action == 'read':
    gist_content = read_gist()
    if gist_content and "hash2ip.txt" in gist_content["files"]:
        file_content = gist_content["files"]["hash2ip.txt"]["content"]
        lines = file_content.splitlines()
        for line in lines:
            if line.startswith(hash_value):
                result = line
                break
        if not result:
            result = f"Hash {hash_value} not found"
    else:
        result = "hash2ip.txt not found"
elif action == 'modify':
    gist_content = read_gist()
    if gist_content and "hash2ip.txt" in gist_content["files"]:
        file_content = gist_content["files"]["hash2ip.txt"]["content"]
        lines = file_content.splitlines()
        updated_lines = []
        found = False
        for line in lines:
            if line.startswith(hash_value):
                updated_lines.append(f"{hash_value},{ip_value}")
                found = True
            else:
                updated_lines.append(line)
        if not found:
            result = f"Hash {hash_value} not found"
        else:
            updated_content = "\n".join(updated_lines)
            success = write_gist(updated_content)
            if success:
                result = "Content updated successfully"
            else:
                result = "Failed to update content"
    else:
        result = "hash2ip.txt not found"
elif action == 'add':
    gist_content = read_gist()
    if gist_content and "hash2ip.txt" in gist_content["files"]:
        file_content = gist_content["files"]["hash2ip.txt"]["content"]
        new_line = f"{hash_value},{ip_value}"
        if any(line.startswith(hash_value) for line in file_content.splitlines()):
            result = f"Hash {hash_value} already exists"
        else:
            updated_content = file_content + "\n" + new_line
            success = write_gist(updated_content)
            if success:
                result = "Content added successfully"
            else:
                result = "Failed to add content"
    else:
        result = "hash2ip.txt not found"

# Imprimir el resultado
print(result)
