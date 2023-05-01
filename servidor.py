import socket
import struct


def receive_file_size(sck: socket.socket):
    #Función que recibe los bytes indicados del archivo a recibir
    
    #En la variable fmt, es el formato que usara la libreria struct para recibir los datos
    fmt = "<Q"
    #Recibimos los bytes indicados del archivo por el cliente
    # En este caso recibimos un little-endian de 64 bits 
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    #Empezamos a recibir los bytes 
    while received_bytes < expected_bytes:
        #En cada iteración se recibe un chunk de bytes 
        chunk = sck.recv(expected_bytes - received_bytes)
        #Se añade el chunk al stream
        stream += chunk
        received_bytes += len(chunk)
    #Se desempaqueta los datos recibidos en el formato deseado que es unsigned int de 64 bits
    filesize = struct.unpack(fmt, stream)[0]

    return filesize


def receive_file(sck: socket.socket, filename):
    # Leemos los bytes que recibiremos del archivo
    filesize = receive_file_size(sck)
    # Abrir un nuevo archivo en donde guardar los datos recibidos.
    try:
        with open(filename, "wb") as f:
            received_bytes = 0
            #Recibiremos los datos del archivo en bloques de 1024 bytes, hasta que se complete
            while received_bytes < filesize:
                chunk = sck.recv(1024)
                if chunk:
                    f.write(chunk)
                    received_bytes += len(chunk)
    except FileNotFoundError:
        print(f'No se encontró el archivo {filename}')
        conn.sendall('No se encontró el archivo solicitado'.encode("utf-8"))


def mount_server():
    while True:    
        with socket.create_server(("localhost", 6190)) as server:
            #Ponemos en estado de escucha
            print("Esperando al cliente...")

            #Aceptamos la conexión
            global conn
            conn, address = server.accept()
            print(f"{address[0]}:{address[1]} conectado.")
            data = conn.recv(1024)

            if not data:
                print('No se recibió la solicitud del archivo')
                conn.sendall('No se recibió la solicitud del archivo'.encode("utf-8"))
                exit()
            
            #Obtenemos el nombre del archivo
            filename = data.decode()

            print("Recibiendo archivo...")
            receive_file(conn, f"new_{filename}")
            print("Archivo recibido.")

if __name__ == "__main__":
    mount_server()