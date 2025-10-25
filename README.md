#🍕 PixelPizza SuperBackend

PixelPizza SuperBackend is a powerful backend for a pizza ordering platform
It consists of two main parts:

1. API Layer — the main backend for the pizza website (Node.js, Express, and MongoDB)


2. Agent (Admin Panel) — a Telegram bot built with Python and Aiogram




---

##⚙️ API Layer

The API handles all the core features of the pizza ordering system, including:

- Menu management (add, edit, delete pizza items)

- Cart management (add or remove items from the cart)

- Order management (create, update, and track orders)

- User management (authentication, roles, profile, etc.)

- JWT-based authentication

- RESTful architecture



---

##🤖 Agent (Telegram Admin Panel)

The Agent is a Telegram bot written in Python using Aiogram.
It provides a simple and powerful way to manage your website directly from Telegram.

Features:

- Instant notifications for new orders

- View and manage orders directly within Telegram

- Manage users

- Add or remove menu items

- Update order status instantly

- View site statistics and analytics, such as:

> Most ordered pizza items

> Top customers with the highest number of orders

> Total sales overview

> and more...

In short:
> You can manage your entire pizza business from Telegram!



---
##🚀 Getting Started

After cloning the repository, you will have two separate folders:

PixelPizzaAPI → the backend API

PixelPizzaAgent → the Telegram admin bot


Both folders have their own config.env.example files. Make sure to configure both before running anything.

-1️⃣ Clone the repository

```
git clone https://github.com/YasinH4010/PixelPizza-SuperBackend.git
cd PixelPizza-SuperBackend
```

-2️⃣ Set up environment variables

PixelPizzaAPI & PixelPizzaAgent → copy `config.env.example` to `config.env` and set values



-3️⃣ Install dependencies

For the API (Node.js)

```
cd PixelPizzaAPI
npm install
```


-4️⃣ Run the services

Run API:

```
cd PixelPizzaAPI
node server.js
```

Run Telegram Bot (Agent):

```
cd PixelPizzaAgent
python3 bot.py
```

> ✅ Make sure both services are running if you want full functionality.



---
