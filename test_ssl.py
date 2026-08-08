import ssl
import socket

host = "26b127e5.databases.neo4j.io"
port = 7687

context = ssl.create_default_context()

try:
    sock = socket.create_connection((host, port))
    ssock = context.wrap_socket(sock, server_hostname=host)

    print("✅ SSL connection successful")
    print("Certificate subject:")
    print(ssock.getpeercert())

    ssock.close()

except Exception as e:
    print("❌ SSL Error")
    print(e)