from flask import Flask, render_template, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "melody18"
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_result():
    with driver.session() as session:
        result = session.run("MATCH (n:Junction {name: 'a'}) RETURN n.result AS result")
        result_array = result.single()["result"]
        return result_array

@app.route('/')
def index():
    result_array = get_result()
    return render_template('index.html', result_array=result_array)

@app.route('/check-connection', methods=['GET'])
def check_connection():
    result_array = get_result()
    return jsonify({
        'status': 'connected',
        'result_array': result_array
    })

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, jsonify
# from neo4j import GraphDatabase

# app = Flask(__name__)

# # Neo4j connection details
# uri = "bolt://localhost:7687"
# username = "neo4j"
# password = "melody18"
# driver = GraphDatabase.driver(uri, auth=(username, password))

# # Function to retrieve result from Neo4j
# def get_result():
#     with driver.session() as session:
#         result = session.run("MATCH (n:Junction {name: 'a'}) RETURN n.result AS result")
#         record = result.single()
#         if record:
#             result_array = record["result"]
#             return result_array
#         else:
#             return "No data found"

# # Root route
# @app.route('/')
# def index():
#     result_array = get_result()
#     return render_template('index.html', result_array=result_array)

# # Route to check connection
# @app.route('/check-connection', methods=['GET'])
# def check_connection():
#     try:
#         result_array = get_result()
#         return jsonify({
#             'status': 'connected',
#             'result_array': result_array
#         })
#     except Exception as e:
#         return jsonify({
#             'status': 'connection failed',
#             'error': str(e)
#         })

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
