# Coderr App – REST API Documentation

Coderr is a freelance service platform that connects businesses with skilled
developers. It provides a RESTful API built with Django REST Framework and
Python.

The API includes endpoints for authentication, profiles, offers, orders,
reviews, and base information.

Please note: This project was developed as part of a personal portfolio to
showcase backend development skills.

---

## 🌐 Base URL

This project is currently under development.

> Open the project in **Visual Studio Code**.
> Open a new terminal and enter

```
git clone https://github.com/ProRuan/coderr.git

cd ./coderr/

python -m venv env

"env/Scripts/activate"

pip install -r requirements.txt

pip freeze

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```

> Access the API via your local domain (e.g. `http://127.0.0.1:8000/api/`).

---

## ❗ Coderr Frontend

You can find the Coderr frontend project here:

**GitHub**:
https://github.com/Developer-Akademie-Backendkurs/project.Coderr

To use the guest account, update the `config.js` file found at  
`/shared/scripts/config.js`. Set your guest login as shown:

```
const GUEST_LOGINS = {
    customer: {
        username: "morgan.taylor@example.com",
        password: "Test123!"
    },
    business: {
        username: "morgan.taylor@example.com",
        password: "Test123!"
    },
}
```

---

## 🔐 Authentication

This API uses **token-based authentication**.

- Register and obtain a token via the `/api/registration/` endpoint (POST).
- Include the token in the `Authorization` header of all requests:

```
Authorization: Token your_token_here
```

## 🚫 Permissions

- Only **authenticated users** can access the API.
- Users can only **view and modify** created or related resources.

---

## 📣 Contact

If you encounter issues or have questions, feel free to reach out:

**Name**: Rudolf Johann Sachslehner
**Email**: rudolf.sachslehner@gmx.at
**GitHub**: https://github.com/ProRuan
