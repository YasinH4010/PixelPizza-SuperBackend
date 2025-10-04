const express = require('express')
const { deleteItem, editItem, addItem, getItem } = require('../Controller/itemController')
const {getItems} = require(`${__dirname}/../Controller/itemController`)
const withAuth = require("../utils/reqAuth");

const Router = express.Router()


Router
.route('/')
.get(...withAuth('getItems'), getItems)

Router
.route('/:id')
.get(...withAuth('getItems'), getItem)

Router
.route('/deleteItem/:id')
.delete(...withAuth('deleteItems'), deleteItem)

Router
.route('/editItem/:id')
.patch(...withAuth('editItems'), editItem)

Router
.route('/addItem')
.post(...withAuth('addItems'), addItem)

module.exports = Router