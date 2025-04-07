
# 🛍️ E-Shop – Django E-commerce Platform

A fully functional e-commerce web application built with **Django** and **SQLite**, designed with a custom admin panel, user ticketing system, product management, and real-time order notifications.  
This project is ideal for learning full-stack development using Django or as a solid base for launching your own online store.

---

## 🔥 Features

### 🛒 Public Features (Users)
- Register, login, and manage user profile
- Browse products with detailed views
- Add/remove items to/from cart
- Submit product reviews
- Create and manage support tickets
- Receive notifications when order status changes

### 🔐 Admin Panel (Custom Built – Not Django Default)
- Review, approve or reject user orders
- Add, edit, and delete products
- Manage and respond to user support tickets
- Full dashboard interface (separate from Django admin)

---

## 🛠️ Tech Stack

| Layer         | Technology        |
|---------------|-------------------|
| Backend       | Django             |
| Frontend      | HTML, CSS, JavaScript (customized template) |
| Database      | SQLite             |
| Authentication | Django built-in auth |
| Styling       | Bootstrap-based template (heavily customized) |

---

Note:to use this app,you can either download this project and use python manage.py runserver in vscode or pycharm to run the app on your localhost,
or you can pull it's docker image by this command,docker pull sadrajaf77/eshop:latest and the create a container for it.
there is also a dockerfile in the projects main directory,use that to create your own image for this app if you needed to.



