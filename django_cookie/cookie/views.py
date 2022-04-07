from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from random import choice
from cookie.helperfunctions import generateFernet, encrypt, decrypt

# set cookies
# get cookies
# delete cookies

key = b"7ZGS7-c5EdesRwUUkCfHxIJyVMbAW7rT1Fk6ethFu4c="
keyList = [
    b"RYWAQLfdmY65UFefqAJcRW0WEfrtrBTUPkl3nlV_PC4=",
    b"9jRsOPoL9LCzCxlYQY7udcBuS0qwseQVFjLhQGU7mDc=",
    b"XdugiKAMbOkfFn3mK7ldVBaW2hIA5ZX0kGfZA6CwAz4=",
    b"6DvLLuzyjNqq3r6buSitPoZEmAzOl2qW7ztPoqEt8vE=",
    b"hV9rhFLc3_0ahMz-p5r1ET7-VO11baSOP0LSBAf9jRg=",
]
active = []


def login(request):
    global key
    globalf = generateFernet(key)

    if request.method == "GET":
        # getting cookies
        if (
            "timer" in request.COOKIES
            and "logged_in" in request.COOKIES
            and "username" in request.COOKIES
        ):
            context = {
                "username": request.COOKIES["username"],
                "login_status": request.COOKIES.get("logged_in"),
                "users": ", ".join(active),
            }
            curKey = context["username"][2:-1]
            username = curKey[140:].encode()
            curKey = decrypt(globalf, curKey[0:140].encode())
            localf = generateFernet(curKey)
            print("Before Decryption =", username)
            username = decrypt(localf, username).decode()
            print("After Decryption =", username)
            context["username"] = username
            return render(request, "home.html", context)
        else:
            response = render(request, "login.html")
            response.delete_cookie("username")
            response.delete_cookie("logged_in")
            return response

    if request.method == "POST":
        username = request.POST.get("email")
        active.append(username)
        print("First Login =", username)
        context = {
            "username": username,
            "login_status": "TRUE",
            "users": ", ".join(active),
        }
        response = render(request, "home.html", context)

        # Adding name to active users

        # setting cookies

        curKey = keyList[choice([0, 1, 2, 3, 4])]
        localf = generateFernet(curKey)
        curKey = encrypt(globalf, curKey)
        username = username.encode()
        username = encrypt(localf, username)
        print("Name stored in cookie =", username)
        username = curKey + username
        print("Name stored in cookie with appending =", username)
        response.set_cookie("username", username)
        response.set_cookie("logged_in", True)
        response.set_cookie("timer", True, max_age=60000)
        return response


def home(request):
    global key
    f = generateFernet(key)

    if "logged_in" in request.COOKIES and "username" in request.COOKIES:
        context = {
            "username": request.COOKIES["username"],
            "login_status": request.COOKIES.get("logged_in"),
        }
        print("Before Decryption =", context["username"])
        context["username"] = decrypt(f, context["username"][2:-1].encode()).decode()
        print("After Decryption =", context["username"])
        return render(request, "home.html", context)
    else:
        return render(request, "home.html")


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
        print(active)
        active.remove(username)
        print(active)
        print("Removed username")

    # deleting cookies
    response.delete_cookie("username")
    response.delete_cookie("logged_in")
    response.delete_cookie("timer")

    return response
