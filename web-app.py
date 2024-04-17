from flask import Flask, render_template, jsonify
import json
import os
import time

app = Flask(__name__)

nodes_file = "nodes.json"
links_file = "links.json"
key_file = "key.json"
theme_file = "theme.json"

def load_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

# Read initial nodes, links, key, and theme data
nodes = load_json(nodes_file)
links = load_json(links_file)
key = load_json(key_file)
theme = load_json(theme_file)

def check_file_changes():
    global nodes, links, key, theme
    while True:
        # Check modification time of nodes file
        nodes_modified_time = os.path.getmtime(nodes_file)
        if nodes_modified_time > os.path.getmtime(links_file):
            # Nodes file has been modified
            nodes = load_json(nodes_file)
            links = load_json(links_file)
            print("Nodes file updated. Reloading data...")
        # Check modification time of links file
        links_modified_time = os.path.getmtime(links_file)
        if links_modified_time > os.path.getmtime(nodes_file):
            # Links file has been modified
            nodes = load_json(nodes_file)
            links = load_json(links_file)
            print("Links file updated. Reloading data...")
        # Check modification time of key file
        key_modified_time = os.path.getmtime(key_file)
        if key_modified_time > max(nodes_modified_time, links_modified_time):
            # Key file has been modified
            key = load_json(key_file)
            print("Key file updated. Reloading data...")
        # Check modification time of theme file
        theme_modified_time = os.path.getmtime(theme_file)
        if theme_modified_time > max(nodes_modified_time, links_modified_time, key_modified_time):
            # Theme file has been modified
            theme = load_json(theme_file)
            print("Theme file updated. Reloading data...")
        time.sleep(5)  # Check every 5 seconds

@app.route('/')
def index():
    return render_template('app-index.html', nodes=nodes, links=links, key=key, theme=theme)

@app.route('/nodes')
def get_nodes():
    return jsonify(nodes)

@app.route('/links')
def get_links():
    return jsonify(links)

@app.route('/key')
def get_key():
    return jsonify(key)

if __name__ == '__main__':
    # Start the file change checker thread
    import threading
    file_change_checker = threading.Thread(target=check_file_changes)
    file_change_checker.daemon = True
    file_change_checker.start()

    app.run(debug=True, host="0.0.0.0", port="8501")
