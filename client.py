import os
import socket
import struct

filename = "matriz.py"

def send_file(sck: socket.socket, filename):
    # Obtener el tamaño del archivo a enviar.
    filesize = os.path.getsize(filename)
    # Informamos al servidor cuantos bytes se van a enviar
    sck.sendall(struct.pack("<Q", filesize))
    # Enviar el archivo en bloques de 1024 bytes.
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)


with socket.create_connection(("localhost", 6190)) as conn:
    #Conectamos con el servidor
    print("Conectado al servidor.")
    
    #Enviamos la solicitud al servidor con el nombre encodeado
    conn.sendall(filename.encode())

    #Mandamos a llamar a la función enviar archivo
    print("Enviando archivo...")
    send_file(conn, filename)
    print("Enviado.")

print("Conexión cerrada.")