import requests
import argparse

# Configuración de los argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Manage Gists')
parser.add_argument('--token', required=True, help='GitHub token')
parser.add_argument('--id', required=True, help='Gist ID')

args = parser.parse_args()
gist_id = args.id
token = args.token

# Imprimir los valores de los argumentos para depuración
print(f"GIST_ID: {gist_id}")
print(f"TOKEN: {token[:5]}... (truncated)")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Función para leer el contenido del gist
def read_gist():
    print(f"Reading gist with ID: {gist_id}")
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
    if response.status_code == 200:
        gist_content = response.json()
        print("Gist content:", gist_content)
        return gist_content
    else:
        print(f"Error: {response.status_code}")
        return None

# Función para escribir contenido en el gist
def write_gist(content):
    print(f"Writing to gist with ID: {gist_id}")
    data = {
        "files": {
            "example.txt": {
                "content": content
            }
        }
    }
    response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)
    if response.status_code == 200:
        print("Gist updated successfully")
    else:
        print(f"Error: {response.status_code}")

# Leer el contenido actual del gist
gist_content = read_gist()

# Escribir nuevo contenido en el gist
if gist_content:
    new_content = "Hello, modified world!"
    write_gist(new_content)
