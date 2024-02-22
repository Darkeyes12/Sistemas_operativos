import random
import time
import tkinter as tk

class BufferApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x300")
        self.root.configure(background='black')
        self.root.title("Productor-Consumidor")
        self.label = tk.Label(root, text="Productor-Consumidor",fg="light green",bg="black", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.buffer_list = ["__"] * 20
        self.indice_productor = 0
        self.indice_consumidor = 0

        self.buffer_title = tk.Label(root, text="",fg="white",bg="black", font=("Helvetica", 12, "bold"))
        self.buffer_title.pack()
        self.buffer_label = tk.Label(root, text="",fg="light green",bg="black", font=("Helvetica", 12))
        self.buffer_label.pack(pady=20)
        self.action_label = tk.Label(root, text="",fg="white",bg="black", font=("Helvetica", 12, "bold"))
        self.action_label.pack()
        self.elementos_label = tk.Label(root, text="",fg="white",bg="black", font=("Helvetica", 12, "bold"))
        self.elementos_label.pack()

        self.update_display()

    def productor(self):
        self.buffer_list, self.indice_productor = productor(self.buffer_list, self.indice_productor)
        self.update_display()

    def consumidor(self):
        self.buffer_list, self.indice_consumidor = consumidor(self.buffer_list, self.indice_consumidor)
        self.update_display()

    def update_display(self):
        buffer_title = "Buffer: "
        self.buffer_title.config(text=buffer_title)
        buffer_text= "   ".join(self.buffer_list)
        self.buffer_label.config(text=buffer_text)
        action_text = "\nProductor: Dormido\nConsumidor: Dormido"
        opcion = random.randrange(1, 3)
        if opcion == 1:
            self.buffer_list, self.indice_productor,self.action_label,self.elementos_label = productor(self)
        elif opcion == 2:
            self.buffer_list, self.indice_consumidor,self.action_label,self.elementos_label = consumidor(self)
        time.sleep(.5)
        self.root.after(100, self.update_display)  # Update every 500 milliseconds

def cerrar_programa(event):
        root.destroy()

def id_lista():
    x = 57
    for i in range(1, 21):
        label = tk.Label(root, fg="light green",bg="black", font=("Helvetica", 12, "bold"), text=str(i))
        label.place(x=x, y=140)
        x += 30

def productor(self):
    # Lógica del productor
    if self.buffer_list[self.indice_productor] == " II  ":
        action_text = "\nProductor: Intentando entrar\nConsumidor: Dormido"
        self.action_label.config(text=action_text)
        elementos_text = "No hay elementos disponibles"
        self.elementos_label.config(text=elementos_text)
        time.sleep(.5)
        return self.buffer_list,self.indice_productor,self.action_label,self.elementos_label
    else:
        producto = random.randrange(4,7)
        for _ in range(producto):
            if self.buffer_list[self.indice_productor] == "__":
                action_text = "\nProductor: Trabajando\nConsumidor: Dormido"
                self.action_label.config(text=action_text)
                elementos_text = "Si hay elementos disponibles"
                self.elementos_label.config(text=elementos_text)
                self.buffer_list[self.indice_productor] = " II  "
                self.indice_productor += 1
                if self.indice_productor == 20:
                    self.indice_productor = 0
            else:
                action_text = "\nProductor: Intentando entrar\nConsumidor: Dormido"
                self.action_label.config(text=action_text)
                elementos_text = "No hay elementos disponibles"
                self.elementos_label.config(text=elementos_text)
            time.sleep(.5)
        if self.indice_productor == 19:
            self.indice_productor = 0   
        return self.buffer_list,self.indice_productor,self.action_label,self.elementos_label

def consumidor(self):
    # Lógica del consumidor
    if self.buffer_list[self.indice_consumidor] == "__":
        action_text = "\nProductor: Dormido\nConsumidor: Intentando entrar"
        self.action_label.config(text=action_text)
        elementos_text = "No hay elementos disponibles"
        self.elementos_label.config(text=elementos_text)
        time.sleep(.5)
        return self.buffer_list,self.indice_consumidor,self.action_label,self.elementos_label
    else:
        consumido = random.randrange(4,7)
        for _ in range(consumido):
            if self.buffer_list[self.indice_consumidor] == " II  ":
                action_text = "\nProductor: Dormido\nConsumidor: Consumiendo"
                self.action_label.config(text=action_text)
                elementos_text = "Si hay elementos disponibles"
                self.elementos_label.config(text=elementos_text)
                self.buffer_list[self.indice_consumidor] = "__"
                self.indice_consumidor += 1
                if self.indice_consumidor == 20:
                    self.indice_consumidor = 0
            else:
                action_text = "\nProductor: Dormido\nConsumidor: Intentando entrar"
                self.action_label.config(text=action_text)
                elementos_text = "No hay elementos disponibles"
                self.elementos_label.config(text=elementos_text)

            time.sleep(.5)
        if self.indice_consumidor == 19:
            self.indice_consumidor = 0
        return self.buffer_list,self.indice_consumidor,self.action_label,self.elementos_label

root = tk.Tk()
app = BufferApp(root)
id_lista()  # Coloca los números en la ventana
root.bind('<Escape>', cerrar_programa)
root.mainloop()

