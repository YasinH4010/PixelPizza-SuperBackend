const express = require('express');
const { getProfile } = require('../Controller/authController');
const { getUsers, deleteUser, getuser, editUser } = require('../Controller/userController');
const {signup, login, protect} = require(`${__dirname}/../Controller/authController`)
const withAuth = require("../utils/reqAuth");

const Router = express.Router()

Router
.route('/')
.get(...withAuth('getUsers'), getUsers)

Router
.route('/:id')
.get(...withAuth('getUsers'), getuser)

Router
.route('/deleteUser/:id')
.delete(...withAuth('deleteUsers'), deleteUser)

Router
.route('/editUser/:id')
.patch(...withAuth('editUsers'), editUser)

module.exports = Router