from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from random import choice
from cookie.helperfunctions import generateFernet, encrypt, decrypt

# Global key
key = b"7ZGS7-c5EdesRwUUkCfHxIJyVMbAW7rT1Fk6ethFu4c="

# List of Keys
keyList = [
    b"RYWAQLfdmY65UFefqAJcRW0WEfrtrBTUPkl3nlV_PC4=",
    b"9jRsOPoL9LCzCxlYQY7udcBuS0qwseQVFjLhQGU7mDc=",
    b"XdugiKAMbOkfFn3mK7ldVBaW2hIA5ZX0kGfZA6CwAz4=",
    b"6DvLLuzyjNqq3r6buSitPoZEmAzOl2qW7ztPoqEt8vE=",
    b"hV9rhFLc3_0ahMz-p5r1ET7-VO11baSOP0LSBAf9jRg=",
]

# List of active users
active = []

# Login page
def login(request):

    # Global key for encryption
    global key
    globalf = generateFernet(key)

    if request.method == "GET":
        # Checking if timer has expired
        if (
            "timer" in request.COOKIES
            and "logged_in" in request.COOKIES
            and "username" in request.COOKIES
        ):

            # Getting data from cookie
            context = {
                "username": request.COOKIES["username"],
                "login_status": request.COOKIES.get("logged_in"),
                "users": ", ".join(active),
            }

            # Getting current key and username albeit in encrypted form and decrypting
            curKey = context["username"][2:-1]
            username = curKey[140:].encode()
            curKey = decrypt(globalf, curKey[0:140].encode())
            localf = generateFernet(curKey)
            print("Before Decryption =", username)
            username = decrypt(localf, username).decode()
            print("After Decryption =", username)
            context["username"] = username

            # Rendering
            return render(request, "home.html", context)
        else:
            response = render(request, "login.html")

            # Getting username to delete from list of active users
            if "logged_in" in request.COOKIES and "username" in request.COOKIES:
                curKey = request.COOKIES["username"][2:-1]
                username = curKey[140:].encode()
                curKey = decrypt(globalf, curKey[0:140].encode())
                localf = generateFernet(curKey)
                print("Before Decryption =", username)
                username = decrypt(localf, username).decode()
                print("After Decryption =", username)
                if username in active:
                    active.remove(username)
                    print("Removed username")

            # Deleting cookies
            response.delete_cookie("username")
            response.delete_cookie("logged_in")
            return response

    if request.method == "POST":
        # Getting username
        username = request.POST.get("email")

        # Adding name to active users
        active.append(username)

        # Setting context for rendering
        print("First Login =", username)
        context = {
            "username": username,
            "login_status": "TRUE",
            "users": ", ".join(active),
        }
        response = render(request, "home.html", context)

        # Encrypting username and curKey and then appending curKey to username
        curKey = keyList[choice([0, 1, 2, 3, 4])]
        localf = generateFernet(curKey)
        curKey = encrypt(globalf, curKey)
        username = username.encode()
        username = encrypt(localf, username)
        print("Name stored in cookie =", username)
        username = curKey + username
        print("Name stored in cookie with appending =", username)

        # setting cookies
        response.set_cookie("username", username)
        response.set_cookie("logged_in", True)
        response.set_cookie("timer", True, max_age=100)
        return response


def logout(request):
    globalf = generateFernet(key)
    response = HttpResponseRedirect(reverse("login"))

    # Getting username
    curKey = request.COOKIES["username"][2:-1]
    username = curKey[140:].encode()
    curKey = decrypt(globalf, curKey[0:140].encode())
    localf = generateFernet(curKey)
    print("Before Decryption =", username)
    username = decrypt(localf, username).decode()
    print("After Decryption =", username)
    if username in active:
        active.remove(username)
        print("Removed username")

    # deleting cookies
    response.delete_cookie("username")
    response.delete_cookie("logged_in")
    response.delete_cookie("timer")

    # Rendering page
    return response
