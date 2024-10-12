import mysql.connector
import redis
import config

db = mysql.connector.connect(
    host=config.dbhost,
    user=config.dbuser,
    password=config.dbpass,
)

# Create database and table if not exists
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(config.dbname))
cursor.execute("USE {}".format(config.dbname))
cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_table (
        `key` VARCHAR(255) PRIMARY KEY,
        value VARCHAR(255)
    )
""")
cursor.execute("INSERT INTO test_table (`key`, value) VALUES ('name', 'AnyGroupLLC from RDS') ON DUPLICATE KEY UPDATE value='AnyGroupLLC from RDS'")
db.commit()
cursor.close()
db.close()

# Redis connection
redis_client = redis.Redis(
    host=config.redishost,  # Replace with your Redis endpoint
    port=6379,
    db=0
)
# Insert key-value pair into Redis
redis_client.set('name', 'AnyGroupLLC from Redis Cache')

print("Database and Redis setup completed.")
