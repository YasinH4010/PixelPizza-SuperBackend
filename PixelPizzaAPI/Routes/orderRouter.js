const { default: mongoose } = require("mongoose");
const withAuth = require("../utils/reqAuth");
const { editOrder, manageOrder, viewOrder, getOrders } = require("../Controller/orderCotroller");
const express = require("express");

const Router = express.Router()

Router
.route('/')
.get(...withAuth('manageOrder'), getOrders)

Router
.route('/:id')
.get(...withAuth('viewOrder'), viewOrder)

Router
.route('/manage/:id')
.get(...withAuth('manageOrder'), manageOrder)

Router
.route('/manage/:id')
.patch(...withAuth('manageOrder'), editOrder)

module.exports = Router