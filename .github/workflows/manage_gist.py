import requests
import os

# Configuración
gist_id = "82ca846ad81fee5fd6f95725923e1200"
token = os.getenv("GITHUB_TOKEN")
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Función para leer el contenido del gist
def read_gist():
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
    if response.status_code == 200:
        gist_content = response.json()
        print("Gist content:", gist_content)
    else:
        print(f"Error: {response.status_code}")

# Función para escribir contenido en el gist
def write_gist(content):
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
read_gist()

# Escribir nuevo contenido en el gist
new_content = "Hello, modified world!"
write_gist(new_content)
