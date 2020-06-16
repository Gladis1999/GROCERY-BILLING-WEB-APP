import time
import socket
from flask import Flask, render_template, request, redirect , url_for



def con():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9997)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

#host = '127.0.0.1'
#port = 5557
#s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#s.connect((host,port))

def buy(item):
    message = bytes(item, 'utf-8')
    sock.send(message)
    exists = recieve()
    return exists


def recieve():
    while True:
        data = sock.recv(1024)
        return str(data, 'utf-8')



def more(item):
    message = bytes(item, 'utf-8')
    sock.send(message)
    exists = recieve()
    return exists


def close():
    sock.send(bytes("exit",'utf-8'))
    sock.close()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def grocery():
    try:
        close()
    except:
        pass
    con()
    if request.method == 'POST':
        grocery_item = request.form['grocery_item']
        response = buy(grocery_item)
        if response == "true":
                return redirect('/want')
        else:
            return render_template("grocery.html", message="invalid item")
    else:
        return render_template("grocery.html")

@app.route('/want', methods=['POST', 'GET'])
def nextitem():
    if request.method == 'POST':
        answer = request.form['answer']
        response = more(answer)
        if response == "true":
                return redirect('/')
        else:
            close()
            f= open("prices.txt",'r')
            line=f.readlines() 
            amount=0
            for word in line:
                x=word.strip()
                for i in x.split():
                    amount=amount+int(x)
            return render_template("thank.html",message="Your Total Purchase Amount:"+str(amount))
            
    else:

        return render_template("more.html")



if __name__ == "__main__":
    app.run(debug=True)
#message = input('Enter the Grocery item number ->')
#while True:
     # s.send(message.encode('ascii'))
      #data = s.recv(1024)
      #print('Recieved from the server :', (data.decode('ascii')))
      #ans = input('\nWant to buy more :')
      #if ans == 'y':
            #message = input('Enter the Grocery item number-> ->')
      #else:
            #print("Thank you for purchasing.")
            #break
#s.close()