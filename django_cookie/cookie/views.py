from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from random import choice
from cookie.helperfunctions import generateFernet, encrypt, decrypt

# set cookies
# get cookies
# delete cookies

key = b"7ZGS7-c5EdesRwUUkCfHxIJyVMbAW7rT1Fk6ethFu4c="


def login(request):
    global key
    f = generateFernet(key)

    if request.method == "GET":
        # getting cookies
        if "logged_in" in request.COOKIES and "username" in request.COOKIES:
            context = {
                "username": request.COOKIES["username"],
                "login_status": request.COOKIES.get("logged_in"),
            }
            print("Before Decryption =", context["username"])
            context["username"] = decrypt(
                f, context["username"][2:-1].encode()
            ).decode()
            print("After Decryption =", context["username"])
            return render(request, "home.html", context)
        else:
            return render(request, "login.html")

    if request.method == "POST":
        username = request.POST.get("email")
        print("First Login =", username)
        context = {
            "username": username,
            "login_status": "TRUE",
        }
        response = render(request, "home.html", context)

        # setting cookies
        username = username.encode()
        username = encrypt(f, username)
        print("Name stored in cookie =", username)
        response.set_cookie("username", username)
        response.set_cookie("logged_in", True)
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
    response = HttpResponseRedirect(reverse("login"))

    # deleting cookies
    response.delete_cookie("username")
    response.delete_cookie("logged_in")

    return response
