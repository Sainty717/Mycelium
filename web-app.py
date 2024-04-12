from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Read nodes data from JSON file
with open("nodes.json", "r") as f:
    nodes_content = f.read()
    nodes = json.loads(nodes_content)

# Read links data from JSON file
with open("links.json", "r") as f:
    links_content = f.read()
    links = json.loads(links_content)

@app.route('/')
def index():
    return render_template('app-index.html', nodes=nodes, links=links)

@app.route('/nodes')
def get_nodes():
    return jsonify(nodes)

@app.route('/links')
def get_links():
    return jsonify(links)

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0', port="8501")
