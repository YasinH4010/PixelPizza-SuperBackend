const express = require("express");
const { viewCart, addToCart, deleteFromCart, checkout } = require("../Controller/cartController");
const withAuth = require("../utils/reqAuth");


const Router = express.Router()


Router
.route('/')
.get(...withAuth('viewCart'), viewCart)

Router
.route('/add/:id')
.patch(...withAuth('addToCart'), addToCart)

Router
.route('/delete/:id')
.delete(...withAuth('deleteFromCart'), deleteFromCart)

Router
.route('/checkout')
.post(...withAuth('checkout'), checkout)

module.exports = Router