const express = require("express");
const { updatePassword, updateProfile, getProfile } = require("../Controller/authController");
const withAuth = require("../utils/reqAuth");

const Router = express.Router()

Router
.route('/')
.get(...withAuth('getProfile'), getProfile)

Router
.route('/changePassword')
.patch(...withAuth('user'), updatePassword)

Router
.route('/update')
.patch(...withAuth('user'), updateProfile)

module.exports = Router