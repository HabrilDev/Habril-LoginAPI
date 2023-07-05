import threading

def hello():
    return input("Hi: ")

hell = threading.Thread(target=hello)
hell.start()
print('\nhi')
hell.join()
print("done")