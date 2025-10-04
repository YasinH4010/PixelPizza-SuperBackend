const express = require('express')
const app = express()
const userRouter = require(`${__dirname}/Routes/userRouter`)
const itemRouter = require(`${__dirname}/Routes/itemRouter`)
const cartRouter = require(`${__dirname}/Routes/cartRouter`)
const orderRouter = require(`${__dirname}/Routes/orderRouter`)
const profileRouter = require(`${__dirname}/Routes/profileRouter`)
app.use(express.json())
const {signup, login, forgotPassword, resetPassword, updatePassword} = require(`./Controller/authController`)
const rateLimit = require('express-rate-limit')
const xss = require('xss-clean')
const santinize = require('express-mongo-sanitize')
const { statsSummary } = require("./Controller/statsController");
const AppError = require('./utils/appError')
const {globalError} = require('./Controller/errorController')
const { default: helmet } = require('helmet')

const limiter = rateLimit({
    max: 100,
    windowMs: 60 * 60 * 1000,
    message: 'this IP banned because too many requests, back an hour later'
})
const authLimiter = rateLimit({
  max: 15,
  windowMs: 15 * 60 * 1000, // 15 دقیقه
  message: 'Too many login attempts, try again later'
})

app.use(helmet())
app.use(santinize())
app.use(xss())
app.use('/', limiter)

app.post('/signup', authLimiter, signup)
app.post('/login', authLimiter, login)

app.post('/forgotPassword', authLimiter, forgotPassword)
app.post('/resetPassword/:token', authLimiter, resetPassword)

app.use('/users', userRouter)
app.use('/items', itemRouter)
app.use('/cart', cartRouter)
app.use('/orders', orderRouter)
app.use('/profile', profileRouter)
app.get('/stats/summary', statsSummary)

app.all('*', (req, res, next) => {
  next(new AppError(`Can't find ${req.originalUrl} on this server!`, 404))
})

app.use(globalError)

module.exports = app