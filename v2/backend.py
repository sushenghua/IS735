import requests
import socket
from flask import Flask, request, jsonify
import redis
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host='${dbhost}',
    user='admin',
    password='${dbpass}',
    database='testdb'
)
db = mysql.connector.connect(
    host=config.dbhost,
    user=config.dbuser,
    password=config.dbpass,
)

redis_client = redis.Redis(
    host='${redishost}',
    port=6379,
    db=0
)

@app.route('/api/value', methods=['POST'])
def get_value():
    try:
        data = request.json
        source = data.get('source', 'database')
        # print("request received")
        hostname = socket.gethostname()

        if source == 'cache':
            response = {'backendhost': hostname, 'value': 'In cache'}
            #return jsonify(response), 200
            value = redis_client.get('name')
            if value is None:
                return jsonify({'error': 'Value not found in cache'}), 404
            response['value-source'] = 'cache'
            response['value'] = value.decode('utf-8')
            return jsonify(response), 200

        elif source == 'database':
            response = {'backendhost': hostname, 'value': 'In database'}
            #return jsonify(response), 200
            cursor = db.cursor()
            cursor.execute('SELECT value FROM test_table WHERE \\`key\\`=%s', ('name',))
            result = cursor.fetchone()
            cursor.close()
            if result:
                response['value-source'] = 'database'
                response['value'] = result[0]
                return jsonify(response), 200
            else:
                return jsonify({'error': 'Value not found in database'}), 404

        else:
            return jsonify({'error': 'Invalid source'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)