from tkinter import*
import socket
from tkinter import filedialog
from Crypto.Cipher import AES
import tqdm as tqdm
import os


def resizeImage(img, new_width, new_height):
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = PhotoImage(width=new_width, height=new_height)
    for x in range(new_width):
        for y in range(new_height):
            xOld = int(x*oldWidth/new_width)
            yOld = int(y*oldHeight/new_height)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage


root = Tk()
root.title('FileShare')
root.geometry('500x340+510+110')
root.configure(bg='#f4fdfe')
root.resizable(False, False)


def Send():
    window = Toplevel(root)
    window.title('Send')
    window.geometry('490x360+0+100')
    window.configure(bg='#f4fdfe')
    # window.resizable(False, False)

    def select_file():
        global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File',
                                              filetypes=(('file_type', '*.txt'), ('all files', '*.*')))

    def sender():
        key = b'TheFileTransfers'
        nonce = b'TheFileTransferN'

        cipher = AES.new(key, AES.MODE_EAX, nonce)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9999))

        file_size = os.path.getsize(filename)
        with open(filename, 'rb') as f:
            data = f.read()
        encrypted = cipher.encrypt(data)

        client.send('file.txt'.encode())
        client.send(str(file_size).encode())
        client.sendall(encrypted)
        client.send(b'<END>')
        print('Data has been transmitted successfully...')
        client.close()

        '''s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print(host)
        print('waiting for any incoming connections...')
        conn, addr = s.accept()
        file = open(filename, 'rb')
        file_data = file.read(1024)
        conn.send(file_data)
        print('Data has been transmitted successfully...')'''

    # icon
    image_icon1 = PhotoImage(file='icons/send_1.png')
    window.iconphoto(False, image_icon1)

    Sbackground= PhotoImage(file='icons/send_3.png')
    Sbackground = resizeImage(Sbackground, 490, 360)
    Label(window, image=Sbackground).place(x=-2, y=0)

    host = socket.gethostname()
    Label(window, text=f'ID: {host}', bg='#FFE7BA', fg='black').place(x=180, y=280)

    Button(window, text='+select file', width=10, height=1, font='arial 14 bold', bd=1, bg='#FFEFD5', fg='#000', command=select_file).place(x=60, y=150)
    Button(window, text='SEND', width=8, height=1, font='arial 14 bold', bg='#8B7355', fg='#fff', command=sender).place(x=300, y=150)

    window.mainloop()


def Receive():
    main = Toplevel(root)
    main.title('Receive')
    main.geometry('490x360+1030+100')
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)

    def receiver():
        key = b'TheFileTransfers'
        nonce = b'TheFileTransferN'

        cipher = AES.new(key, AES.MODE_EAX, nonce)

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 9999))
        server.listen()
        print('waiting for any incoming connections...')

        client, addr = server.accept()
        file_name = client.recv(1024).decode()
        print(file_name)
        file_size = client.recv(1024).decode()
        print(file_size)

        file = open(file_name, 'wb')
        done = False
        file_bytes = b''

        progress = tqdm.tqdm(unit='B', unit_scale=True, unit_divisor=1000, total=int(file_size))

        while not done:
            data = client.recv(1024)
            if file_bytes[-5] == b'<END>':
                done = True
            else:
                file_bytes += data
            progress.update(1024)
        print(file_bytes)
        file.write(cipher.decrypt(file_bytes[:-5]))
        file.close()
        client.close()
        server.close()
        print('File has been received successfully...')
        '''ID = SenderID.get()
        filename1 = incoming_file.get()

        s = socket.socket()
        port = 8080
        s.connect((ID, port))
        file = open(filename1, 'wb')
        file_data = s.recv(1024)
        file.write(file_data)
        file.close()
        print('File has been received successfully...')'''

    # icon
    image_icon1 = PhotoImage(file='icons/received_icon.png')
    image_icon1 = resizeImage(image_icon1, 50, 50)
    main.iconphoto(False, image_icon1)

    Hbackground = PhotoImage(file='icons/received_1.png')
    Hbackground = resizeImage(Hbackground, 540, 465)
    Label(main, image=Hbackground).place(x=-50, y=0)

    '''logo = PhotoImage(file='icons/received.gif')
    logo = resizeImage(logo, 50, 50)
    Label(main, image=logo, bg='#f4fdfe').place(x=70, y=50)

    Label(main, text='Receive', font=('arial', 20), bg='#f4fdfe').place(x=100, y=50)'''

    Label(main, text='Input sender id', font=('arial', 10, 'bold'), bg='#f4fdfe').place(x=80, y=90)
    SenderID = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    SenderID.place(x=80, y=110)
    SenderID.focus()

    Label(main, text='Filename for the incoming file: ', font=('arial', 10, 'bold'), bg='#f4fdfe').place(x=80, y=170)
    incoming_file = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    incoming_file.place(x=80, y=190)

    image_icon2 = PhotoImage(file='icons/received.gif')
    image_icon2 = resizeImage(image_icon2, 30, 20)
    rr = Button(main, text=' Receive', compound=LEFT, image=image_icon2, width=100, bg='#33A1C9', font='arial 12 bold', command=receiver)
    rr.place(x=360, y=300)

    main.mainloop()


# icon
image_icon=PhotoImage(file='icons/share.png')
# image_icon = resizeImage(image_icon, 20, 20)
root.iconphoto(False, image_icon)


background= PhotoImage(file='icons/background.png')
background = resizeImage(background, 500, 340)
Label(root, image=background).place(x=-2, y=-2)


Label(root, text='Share it with FileShare :)', font=('SimSun', 18), bg='#F8F8FF').place(x=50, y=50)

Frame(root, width=400, height=2, bg='#f3f5f6').place(x=25, y=80)

send_image = PhotoImage(file='icons/send.png')
send_image = resizeImage(send_image, 70, 70)
send = Button(root, image=send_image, bg='#f4fdfe', bd=0, command=Send)
send.place(x=70, y=120)

receive_image= PhotoImage(file='icons/receive.png')
receive_image = resizeImage(receive_image, 70, 70)
receive= Button(root, image=receive_image, bg='#f4fdfe', bd=0, command=Receive)
receive.place(x=310, y=120)

# label
Label(root, text='Send', font=('Acumin Variable Concept', 13, 'bold'), bg='#f4fdfe').place(x=80, y=210)
Label(root, text='Receive', font=('Acumin Variable Concept', 13, 'bold'), bg='#f4fdfe').place(x=310, y=210)


root.mainloop()
