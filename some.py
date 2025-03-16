import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import cv2
import time
from neo4j import GraphDatabase
import torch
from PIL import Image, ImageTk

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', source='github')

# Function to detect vehicles in an image
def detect_vehicles(image):
    results = model(image)
    detected_objects = results.pred[0]
    labels = detected_objects[:, -1].cpu().numpy()
    vehicle_count = 0
    for label in labels:
        if int(label) in [2, 3, 7]:  # 2: car, 3: motorcycle, 7: truck
            vehicle_count += 1
    return vehicle_count

# Function to detect vehicles in a video
def detect_vehicles_in_video(video_path, duration):
    cap = cv2.VideoCapture(video_path)
    start_time = time.time()
    vehicle_count = 0
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break
        vehicle_count += detect_vehicles(frame)
    cap.release()
    return vehicle_count

# Function to update Neo4j database
def update_neo4j(uri, user, password, incoming_static, outgoing):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        session.run("MATCH (n:Junction {name: 'a'}) SET n.incoming_static = $incoming_static, n.outgoing = $outgoing", 
                    incoming_static=incoming_static, outgoing=outgoing)
    driver.close()

# Function to retrieve result array from Neo4j
def retrieve_results(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    results = []
    with driver.session() as session:
        result = session.run("MATCH (n:Junction {name: 'a'}) RETURN n.result AS result")
        results = result.single()["result"]
    driver.close()
    return results

# Function to run additional Cypher queries
def run_additional_queries(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        # Replace these queries with your own
        # Query 1
        session.run("""// Handle :CONNECTED_TO0
MATCH (x:Junction {name: 'a'})-[:CONNECTED_TO0]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[0]) AS index, x.outgoing[0] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO1
MATCH (x:Junction {name: 'a'})-[:CONNECTED_TO1]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[1]) AS index, x.outgoing[1] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO2
MATCH (x:Junction {name: 'a'})-[:CONNECTED_TO2]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[2]) AS index, x.outgoing[2] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO3
MATCH (x:Junction {name: 'a'})-[:CONNECTED_TO3]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[3]) AS index, x.outgoing[3] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y
UNION

// Handle :CONNECTED_TO0
MATCH (x:Junction {name: 'b'})-[:CONNECTED_TO0]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[0]) AS index, x.outgoing[0] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO1
MATCH (x:Junction {name: 'b'})-[:CONNECTED_TO1]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[1]) AS index, x.outgoing[1] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO2
MATCH (x:Junction {name: 'b'})-[:CONNECTED_TO2]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[2]) AS index, x.outgoing[2] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO3
MATCH (x:Junction {name: 'b'})-[:CONNECTED_TO3]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[3]) AS index, x.outgoing[3] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y
UNION

// Handle :CONNECTED_TO0
MATCH (x:Junction {name: 'c'})-[:CONNECTED_TO0]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[0]) AS index, x.outgoing[0] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO1
MATCH (x:Junction {name: 'c'})-[:CONNECTED_TO1]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[1]) AS index, x.outgoing[1] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO2
MATCH (x:Junction {name: 'c'})-[:CONNECTED_TO2]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[2]) AS index, x.outgoing[2] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO3
MATCH (x:Junction {name: 'c'})-[:CONNECTED_TO3]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[3]) AS index, x.outgoing[3] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y
UNION

// Handle :CONNECTED_TO0
MATCH (x:Junction {name: 'd'})-[:CONNECTED_TO0]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[0]) AS index, x.outgoing[0] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO1
MATCH (x:Junction {name: 'd'})-[:CONNECTED_TO1]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[1]) AS index, x.outgoing[1] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO2
MATCH (x:Junction {name: 'd'})-[:CONNECTED_TO2]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[2]) AS index, x.outgoing[2] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO3
MATCH (x:Junction {name: 'd'})-[:CONNECTED_TO3]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[3]) AS index, x.outgoing[3] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y
UNION

// Handle :CONNECTED_TO0
MATCH (x:Junction {name: 'e'})-[:CONNECTED_TO0]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[0]) AS index, x.outgoing[0] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO1
MATCH (x:Junction {name: 'e'})-[:CONNECTED_TO1]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[1]) AS index, x.outgoing[1] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO2
MATCH (x:Junction {name: 'e'})-[:CONNECTED_TO2]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[2]) AS index, x.outgoing[2] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO3
MATCH (x:Junction {name: 'e'})-[:CONNECTED_TO3]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[3]) AS index, x.outgoing[3] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y
UNION

// Handle :CONNECTED_TO0
MATCH (x:Junction {name: 'f'})-[:CONNECTED_TO0]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[0]) AS index, x.outgoing[0] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO1
MATCH (x:Junction {name: 'f'})-[:CONNECTED_TO1]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[1]) AS index, x.outgoing[1] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO2
MATCH (x:Junction {name: 'f'})-[:CONNECTED_TO2]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[2]) AS index, x.outgoing[2] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO3
MATCH (x:Junction {name: 'f'})-[:CONNECTED_TO3]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[3]) AS index, x.outgoing[3] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y
UNION

// Handle :CONNECTED_TO0
MATCH (x:Junction {name: 'g'})-[:CONNECTED_TO0]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[0]) AS index, x.outgoing[0] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO1
MATCH (x:Junction {name: 'g'})-[:CONNECTED_TO1]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[1]) AS index, x.outgoing[1] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO2
MATCH (x:Junction {name: 'g'})-[:CONNECTED_TO2]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[2]) AS index, x.outgoing[2] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO3
MATCH (x:Junction {name: 'g'})-[:CONNECTED_TO3]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[3]) AS index, x.outgoing[3] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y
UNION

// Handle :CONNECTED_TO0
MATCH (x:Junction {name: 'h'})-[:CONNECTED_TO0]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[0]) AS index, x.outgoing[0] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO1
MATCH (x:Junction {name: 'h'})-[:CONNECTED_TO1]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[1]) AS index, x.outgoing[1] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO2
MATCH (x:Junction {name: 'h'})-[:CONNECTED_TO2]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[2]) AS index, x.outgoing[2] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y

UNION

// Handle :CONNECTED_TO3
MATCH (x:Junction {name: 'h'})-[:CONNECTED_TO3]->(y:Junction)
WITH x, y, toInteger(x.node_edge_determiner[3]) AS index, x.outgoing[3] AS value
WITH x, y, index, value, COALESCE(y.incoming_dynamic, []) AS incoming_dynamic
WITH x, y, index, value, 
     CASE
         WHEN index < size(incoming_dynamic) THEN
             [i IN range(0, size(incoming_dynamic) - 1) |
                 CASE WHEN i = index THEN value ELSE incoming_dynamic[i] END]
         ELSE
             incoming_dynamic + [value]
     END AS updatedArray
SET y.incoming_dynamic = updatedArray
RETURN y""")
        # Query 2
        session.run("""MATCH (j:Junction)
SET j.current_vehicles = [x IN range(0, size(j.incoming_static)-1) | j.incoming_static[x] + j.incoming_dynamic[x]]
RETURN j""")
        # Query 3
        session.run("""// Code for node 'b'
MATCH (a:Junction{name:'a'})
SET a.result = coalesce(a.result, []), a.visited = coalesce(a.visited, [])
WITH a, [i IN range(0, size(a.current_vehicles) - 1) WHERE coalesce(a.visited[i], 0) = 0 | a.current_vehicles[i]] AS unvisited_vehicles
WITH a, unvisited_vehicles, apoc.coll.max(unvisited_vehicles) AS max_value, apoc.coll.sum(unvisited_vehicles) AS total_value
WITH a, unvisited_vehicles, max_value, total_value, toInteger(a.time * max_value / total_value) AS computed_value, apoc.coll.indexOf(a.current_vehicles, max_value) AS max_index
SET a.result = apoc.coll.set(a.result, 1, computed_value)
SET a.result = apoc.coll.set(a.result, 0, max_index)
SET a.visited = apoc.coll.set(a.visited, max_index, 1)
WITH a, computed_value, a.time - computed_value AS new_time
SET a.time = new_time
WITH a, size([i IN range(0, size(a.visited) - 1) WHERE a.visited[i] = 1]) AS visited_count
SET a.visited = CASE WHEN visited_count = size(a.current_vehicles) THEN [i IN range(0, size(a.current_vehicles) - 1) | 0] ELSE a.visited END
WITH a, CASE WHEN a.time < 4 THEN a.default_time ELSE a.time END AS updated_time
SET a.time = updated_time
RETURN a

UNION

// Code for node 'a'
MATCH (a:Junction{name:'b'})
SET a.result = coalesce(a.result, []), a.visited = coalesce(a.visited, [])
WITH a, [i IN range(0, size(a.current_vehicles) - 1) WHERE coalesce(a.visited[i], 0) = 0 | a.current_vehicles[i]] AS unvisited_vehicles
WITH a, unvisited_vehicles, apoc.coll.max(unvisited_vehicles) AS max_value, apoc.coll.sum(unvisited_vehicles) AS total_value
WITH a, unvisited_vehicles, max_value, total_value, toInteger(a.time * max_value / total_value) AS computed_value, apoc.coll.indexOf(a.current_vehicles, max_value) AS max_index
SET a.result = apoc.coll.set(a.result, 1, computed_value)
SET a.result = apoc.coll.set(a.result, 0, max_index)
SET a.visited = apoc.coll.set(a.visited, max_index, 1)
WITH a, computed_value, a.time - computed_value AS new_time
SET a.time = new_time
WITH a, size([i IN range(0, size(a.visited) - 1) WHERE a.visited[i] = 1]) AS visited_count
SET a.visited = CASE WHEN visited_count = size(a.current_vehicles) THEN [i IN range(0, size(a.current_vehicles) - 1) | 0] ELSE a.visited END
WITH a, CASE WHEN a.time < 4 THEN a.default_time ELSE a.time END AS updated_time
SET a.time = updated_time
RETURN a

UNION

// Code for node 'c'
MATCH (a:Junction{name:'c'})
SET a.result = coalesce(a.result, []), a.visited = coalesce(a.visited, [])
WITH a, [i IN range(0, size(a.current_vehicles) - 1) WHERE coalesce(a.visited[i], 0) = 0 | a.current_vehicles[i]] AS unvisited_vehicles
WITH a, unvisited_vehicles, apoc.coll.max(unvisited_vehicles) AS max_value, apoc.coll.sum(unvisited_vehicles) AS total_value
WITH a, unvisited_vehicles, max_value, total_value, toInteger(a.time * max_value / total_value) AS computed_value, apoc.coll.indexOf(a.current_vehicles, max_value) AS max_index
SET a.result = apoc.coll.set(a.result, 1, computed_value)
SET a.result = apoc.coll.set(a.result, 0, max_index)
SET a.visited = apoc.coll.set(a.visited, max_index, 1)
WITH a, computed_value, a.time - computed_value AS new_time
SET a.time = new_time
WITH a, size([i IN range(0, size(a.visited) - 1) WHERE a.visited[i] = 1]) AS visited_count
SET a.visited = CASE WHEN visited_count = size(a.current_vehicles) THEN [i IN range(0, size(a.current_vehicles) - 1) | 0] ELSE a.visited END
WITH a, CASE WHEN a.time < 4 THEN a.default_time ELSE a.time END AS updated_time
SET a.time = updated_time
RETURN a

UNION

// Code for node 'd'
MATCH (a:Junction{name:'d'})
SET a.result = coalesce(a.result, []), a.visited = coalesce(a.visited, [])
WITH a, [i IN range(0, size(a.current_vehicles) - 1) WHERE coalesce(a.visited[i], 0) = 0 | a.current_vehicles[i]] AS unvisited_vehicles
WITH a, unvisited_vehicles, apoc.coll.max(unvisited_vehicles) AS max_value, apoc.coll.sum(unvisited_vehicles) AS total_value
WITH a, unvisited_vehicles, max_value, total_value, toInteger(a.time * max_value / total_value) AS computed_value, apoc.coll.indexOf(a.current_vehicles, max_value) AS max_index
SET a.result = apoc.coll.set(a.result, 1, computed_value)
SET a.result = apoc.coll.set(a.result, 0, max_index)
SET a.visited = apoc.coll.set(a.visited, max_index, 1)
WITH a, computed_value, a.time - computed_value AS new_time
SET a.time = new_time
WITH a, size([i IN range(0, size(a.visited) - 1) WHERE a.visited[i] = 1]) AS visited_count
SET a.visited = CASE WHEN visited_count = size(a.current_vehicles) THEN [i IN range(0, size(a.current_vehicles) - 1) | 0] ELSE a.visited END
WITH a, CASE WHEN a.time < 4 THEN a.default_time ELSE a.time END AS updated_time
SET a.time = updated_time
RETURN a

UNION

// Code for node 'e'
MATCH (a:Junction{name:'e'})
SET a.result = coalesce(a.result, []), a.visited = coalesce(a.visited, [])
WITH a, [i IN range(0, size(a.current_vehicles) - 1) WHERE coalesce(a.visited[i], 0) = 0 | a.current_vehicles[i]] AS unvisited_vehicles
WITH a, unvisited_vehicles, apoc.coll.max(unvisited_vehicles) AS max_value, apoc.coll.sum(unvisited_vehicles) AS total_value
WITH a, unvisited_vehicles, max_value, total_value, toInteger(a.time * max_value / total_value) AS computed_value, apoc.coll.indexOf(a.current_vehicles, max_value) AS max_index
SET a.result = apoc.coll.set(a.result, 1, computed_value)
SET a.result = apoc.coll.set(a.result, 0, max_index)
SET a.visited = apoc.coll.set(a.visited, max_index, 1)
WITH a, computed_value, a.time - computed_value AS new_time
SET a.time = new_time
WITH a, size([i IN range(0, size(a.visited) - 1) WHERE a.visited[i] = 1]) AS visited_count
SET a.visited = CASE WHEN visited_count = size(a.current_vehicles) THEN [i IN range(0, size(a.current_vehicles) - 1) | 0] ELSE a.visited END
WITH a, CASE WHEN a.time < 4 THEN a.default_time ELSE a.time END AS updated_time
SET a.time = updated_time
RETURN a

union

// Code for node 'f'
MATCH (a:Junction{name:'f'})
SET a.result = coalesce(a.result, []), a.visited = coalesce(a.visited, [])
WITH a, [i IN range(0, size(a.current_vehicles) - 1) WHERE coalesce(a.visited[i], 0) = 0 | a.current_vehicles[i]] AS unvisited_vehicles
WITH a, unvisited_vehicles, apoc.coll.max(unvisited_vehicles) AS max_value, apoc.coll.sum(unvisited_vehicles) AS total_value
WITH a, unvisited_vehicles, max_value, total_value, toInteger(a.time * max_value / total_value) AS computed_value, apoc.coll.indexOf(a.current_vehicles, max_value) AS max_index
SET a.result = apoc.coll.set(a.result, 1, computed_value)
SET a.result = apoc.coll.set(a.result, 0, max_index)
SET a.visited = apoc.coll.set(a.visited, max_index, 1)
WITH a, computed_value, a.time - computed_value AS new_time
SET a.time = new_time
WITH a, size([i IN range(0, size(a.visited) - 1) WHERE a.visited[i] = 1]) AS visited_count
SET a.visited = CASE WHEN visited_count = size(a.current_vehicles) THEN [i IN range(0, size(a.current_vehicles) - 1) | 0] ELSE a.visited END
WITH a, CASE WHEN a.time < 4 THEN a.default_time ELSE a.time END AS updated_time
SET a.time = updated_time
RETURN a

UNION

// Code for node 'g'
MATCH (a:Junction{name:'g'})
SET a.result = coalesce(a.result, []), a.visited = coalesce(a.visited, [])
WITH a, [i IN range(0, size(a.current_vehicles) - 1) WHERE coalesce(a.visited[i], 0) = 0 | a.current_vehicles[i]] AS unvisited_vehicles
WITH a, unvisited_vehicles, apoc.coll.max(unvisited_vehicles) AS max_value, apoc.coll.sum(unvisited_vehicles) AS total_value
WITH a, unvisited_vehicles, max_value, total_value, toInteger(a.time * max_value / total_value) AS computed_value, apoc.coll.indexOf(a.current_vehicles, max_value) AS max_index
SET a.result = apoc.coll.set(a.result, 1, computed_value)
SET a.result = apoc.coll.set(a.result, 0, max_index)
SET a.visited = apoc.coll.set(a.visited, max_index, 1)
WITH a, computed_value, a.time - computed_value AS new_time
SET a.time = new_time
WITH a, size([i IN range(0, size(a.visited) - 1) WHERE a.visited[i] = 1]) AS visited_count
SET a.visited = CASE WHEN visited_count = size(a.current_vehicles) THEN [i IN range(0, size(a.current_vehicles) - 1) | 0] ELSE a.visited END
WITH a, CASE WHEN a.time < 4 THEN a.default_time ELSE a.time END AS updated_time
SET a.time = updated_time
RETURN a

UNION
                    
MATCH (a:Junction{name:'h'})
SET a.result = coalesce(a.result, []), a.visited = coalesce(a.visited, [])
WITH a, [i IN range(0, size(a.current_vehicles) - 1) WHERE coalesce(a.visited[i], 0) = 0 | a.current_vehicles[i]] AS unvisited_vehicles
WITH a, unvisited_vehicles, apoc.coll.max(unvisited_vehicles) AS max_value, apoc.coll.sum(unvisited_vehicles) AS total_value
WITH a, unvisited_vehicles, max_value, total_value, toInteger(a.time * max_value / total_value) AS computed_value, apoc.coll.indexOf(a.current_vehicles, max_value) AS max_index
SET a.result = apoc.coll.set(a.result, 1, computed_value)
SET a.result = apoc.coll.set(a.result, 0, max_index)
SET a.visited = apoc.coll.set(a.visited, max_index, 1)
WITH a, computed_value, a.time - computed_value AS new_time
SET a.time = new_time
WITH a, size([i IN range(0, size(a.visited) - 1) WHERE a.visited[i] = 1]) AS visited_count
SET a.visited = CASE WHEN visited_count = size(a.current_vehicles) THEN [i IN range(0, size(a.current_vehicles) - 1) | 0] ELSE a.visited END
WITH a, CASE WHEN a.time < 4 THEN a.default_time ELSE a.time END AS updated_time
SET a.time = updated_time
RETURN a""")
    driver.close()

# Function to process images
def process_images(image_paths, is_incoming):
    vehicle_counts = [detect_vehicles(cv2.imread(image)) for image in image_paths]
    if is_incoming:
        global incoming_static
        incoming_static = vehicle_counts
    else:
        global outgoing
        outgoing = vehicle_counts
    print("Images processed and database updated.")
    
    if not is_incoming:
        update_neo4j(uri, user, password, incoming_static, outgoing)
        print("Incoming Static:", incoming_static)
        print("Outgoing:", outgoing)
        
        # Wait for 30 seconds
        #time.sleep(30)
        
        # Run additional queries
        run_additional_queries(uri, user, password)
        
        # Retrieve result array from Neo4j
        results = retrieve_results(uri, user, password)
        print("Results:", results)
        
        # Wait for the time specified in the result array at index 1
        wait_time = results[1]
        #time.sleep(wait_time)
        
        # Start the process again
        start_process()

# Function to process videos
def process_videos(video_paths, duration):
    vehicle_counts = [detect_vehicles_in_video(video, duration) for video in video_paths]
    global outgoing
    outgoing = vehicle_counts
    update_neo4j(uri, user, password, incoming_static, outgoing)
    print("Incoming Static:", incoming_static)
    print("Outgoing:", outgoing)
    
    # Wait for 30 seconds
    # time.sleep(30)
    
    # Run additional queries
    run_additional_queries(uri, user, password)
    
    # Retrieve result array from Neo4j
    results = retrieve_results(uri, user, password)
    print("Results:", results)
    
    # Wait for the time specified in the result array at index 1
    wait_time = results[1]
    #time.sleep(wait_time)
    
    # Start the process again
    start_process()

# Function to upload images
def upload_images(is_incoming):
    file_paths = filedialog.askopenfilenames(filetypes=[("Image files", ".jpg;.jpeg;*.png")])
    if file_paths:
        process_images(file_paths, is_incoming)

# Function to capture images from camera
def capture_images(is_incoming):
    cap = cv2.VideoCapture(0)
    image_paths = []
    for i in range(4):
        messagebox.showinfo("Capture Image", f"Press 'm' to capture image {i+1}")
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Capture Image', frame)
                if cv2.waitKey(1) & 0xFF == ord('m'):
                    image_path = f"captured_image_{i}.jpg"
                    cv2.imwrite(image_path, frame)
                    image_paths.append(image_path)
                    break
        cv2.destroyAllWindows()  # Close the window after each capture
    cap.release()
    process_images(image_paths, is_incoming)

# Function to capture videos
def capture_videos():
    duration = simpledialog.askinteger("Input", "Enter duration for each video (in seconds):")
    if duration is None:
        return  # User cancelled the input dialog

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to open the camera.")
        return

    video_paths = []
    for i in range(4):
        messagebox.showinfo("Capture Video", f"Press 'm' to start recording video {i+1}")
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to read frame from the camera.")
                break

            cv2.imshow('Capture Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('m'):
                video_path = f"captured_video_{i}.avi"
                out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
                start_time = time.time()
                while time.time() - start_time < duration:
                    ret, frame = cap.read()
                    if not ret:
                        messagebox.showerror("Error", "Failed to read frame from the camera.")
                        break

                    out.write(frame)
                    cv2.imshow('Recording Video', frame)  # Display the frame while recording
                    if cv2.waitKey(1) & 0xFF == ord('m'):
                        break

                out.release()
                video_paths.append(video_path)
                break

        cv2.destroyAllWindows()  # Close the window after each capture

    cap.release()
    process_videos(video_paths, duration)

# Function to choose method for incoming_static
def choose_incoming_method():
    choice = simpledialog.askinteger("Input", "Choose method for incoming_static:\n1. Capture 4 images\n2. Upload 4 images")
    if choice == 1:
        capture_images(True)
    elif choice == 2:
        upload_images(True)

# Function to choose method for outgoing
def choose_outgoing_method():
    choice = simpledialog.askinteger("Input", "Choose method for outgoing:\n1. Capture 4 images\n2. Upload 4 images\n3. Capture 4 videos")
    if choice == 1:
        capture_images(False)
    elif choice == 2:
        upload_images(False)
    elif choice == 3:
        capture_videos()

# Function to start the process
def start_process():
    print("upload images__")
    # Choose methods for incoming_static and outgoing
    choose_incoming_method()
    choose_outgoing_method()

# GUI setup
root = tk.Tk()
root.title("Vehicle Detection")

# Localhost connection details
uri = "bolt://localhost:7687"
user = "neo4j"
password = "melody18"  # Replace with your Neo4j password

incoming_static = []
outgoing = []

incoming_button = tk.Button(root, text="Set Incoming Static", command=choose_incoming_method)
incoming_button.pack(pady=10)

outgoing_button = tk.Button(root, text="Set Outgoing", command=choose_outgoing_method)
outgoing_button.pack(pady=10)

# Start the process initially
start_process()

root.mainloop()