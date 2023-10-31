# import all the required  modules
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

 
PORT = 9999 #inserir porta da maquina do servidor
SERVER = 'localhost' #inserir ip da maquina do servidor
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
HEADER = 64
 
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS) 
 
 
class GUI:

    def __init__(self):
 
        self.Window = Tk()
        self.Window.withdraw()
 
        self.login = Toplevel()
    
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
   
        self.pls = Label(self.login,
                         text="Faça o login para continuar",
                         justify=CENTER,
                         font="Helvetica 14 bold")
 
        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
       
        self.labelName = Label(self.login,
                               text="Nome: ",
                               font="Helvetica 12")
 
        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)
 
      
        self.entryName = Entry(self.login,
                               font="Helvetica 14")
 
        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
 

        self.entryName.focus()
 
  
        self.go = Button(self.login,
                         text="Entrar",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))
 
        self.go.place(relx=0.4,
                      rely=0.55)
        self.Window.mainloop()
 
    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
 

        rcv = threading.Thread(target=self.receive)
        rcv.start()
 

    def layout(self, name):
 
        self.name = name
     
        self.Window.deiconify()
        self.Window.title("Sala de conversa")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)
 
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")
 
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
 
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Enviar",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")
 
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
 
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # Exiba a mensagem recebida na caixa de texto
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # Em caso de erro, mostre uma mensagem de erro
                messagebox.showerror("Erro", "Mensagem não recebida")
                client.close()
                break
 
    # Função para enviar mensagens
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            msg = (f"{self.msg}").encode(FORMAT)
            send_len = str(len(msg)).encode(FORMAT)
            send_len += b' ' * (HEADER - len(send_len))
            try:
                client.send(send_len)
                client.send(msg)
                # Exiba a mensagem enviada na caixa de texto
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, f"{self.name}: {self.msg}\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
            except:
                # Em caso de erro, mostre uma mensagem de erro
                messagebox.showerror("Erro", "Mensagem não enviada")
            break
 
 
# create a GUI class object
g = GUI()
