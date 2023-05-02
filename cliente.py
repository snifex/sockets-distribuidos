from tkinter import *
from customtkinter import *
import os
import socket
import struct

def check_content(event):
    if(len(path_entry.get()) > 0):
        send_button.configure(state="normal")
    else:
        send_button.configure(state="disabled")


def browse_file():
    global filename
    #Abrimos un filedialog para buscar en el directorio
    filename = filedialog.askopenfilename()
    filename = filename.split("/")[-1]
    path_entry.delete(0,END)
    path_entry.insert(0,filename)

def send_file_button():

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


set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Propiedades de la ventana
app = CTk();
app.geometry(f"{500}x{300}")
app.resizable(False, False)
app.title("Cliente ventana")

#Centramos la ventana
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculamos la posición
x = int((screen_width - app.winfo_reqwidth()) / 2)
y = int((screen_height - app.winfo_reqheight()) / 2)

# Seteamos con esas coordenadas
app.geometry("+{}+{}".format(x, y))

myFont = CTkFont(family="Montserrat", size=20)



#Creamos un frame
frame = CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

#Creamos los widgets necesarios
path_label = CTkLabel(master=frame, justify=LEFT, text="Ruta del archivo:", font=myFont)
path_label.pack(pady=10, padx= 10)
path_entry = CTkEntry(master=frame, width= 500)
path_entry.pack(pady=10,padx=10)
browse_button = CTkButton(master=frame, command=browse_file, text="Buscar archivo", font=("Arial",12))
browse_button.pack(pady=10,padx=10)
send_button = CTkButton(master=frame, command=send_file_button, text="Enviar archivo", font=("Arial",12), state="disabled")
send_button.pack(pady=10,padx=10)

browse_button.bind("<Button-1>",check_content)
if __name__ == "__main__":
    app.mainloop()
    