const mongoose = require('mongoose')
const AppError = require('../utils/appError')
const bcrypt = require('bcryptjs')
const validator = require('validator')
const crypto = require('crypto')
const Cart = require('./cartModel')

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'required error'],
        unique: [true, 'unique error'],
        minLength: [2, 'pls enter a name with +2 characters'],
        maxLength: [20, 'pls enter a name with -20 characters'],
    },
    email: {
        type: String,
        required: [true, 'required error'],
        unique: [true, 'unique error'],
        validate: [validator.isEmail, 'Please provide a valid email']
    },
    address: String,
    password: {
        type: String,
        select: false,
        required: [true, 'required error'],
        minLength: [8, 'pls enter a password with +8 characters'],
        maxLength: [40, 'pls enter a password with -40 characters']
    },
    cart:{
        type: mongoose.Schema.ObjectId,
        ref: 'Cart'
    },
    permissions: {
        type: [String],
        default: []
    },
    passwordResetToken: String,
    passwordResetExpire: Date,
    passwordChangedAt: Date,
    lastSeen: {
        type: Date,
        default: Date.now
    },
    joinedAt: Date
})
userSchema.virtual('passwordConfirm')

userSchema.pre('save', function(next){
    if(!this.isModified('password')) return next()
    if(this.passwordConfirm!==this.password){
        return next(new AppError('password confirm not match', 401))
    }
    
    next()
})

userSchema.pre('save', async function(next){
    if(!this.isModified('password')) return next()
    this.joinedAt = Date.now()
    console.log(this.password)
    this.password = await bcrypt.hash(this.password, 12)

    next()
})

userSchema.pre('save', async function(next) {
    try{
        if(this.cart) return next();
        const cart = await Cart.create({
        owner: this._id
    })
    this.cart = cart._id
    }catch(err){
        console.log(err)
        return next(new AppError('error in creating user cart', 400))
    }
    next()
})

userSchema.methods.correctPassword = async function(candidatePassword, userPassword) {
    return await bcrypt.compare(candidatePassword, userPassword)
}
userSchema.methods.changedPasswordAfter = async function(JWTTimestamp) {
    const passwordChangedTime = Math.round(this.passwordChangedAt.getTime() / 1000)
    console.log(passwordChangedTime, JWTTimestamp)
    console.log(JWTTimestamp < passwordChangedTime)
    return JWTTimestamp < passwordChangedTime
    
    // return false
}
userSchema.methods.createResetToken = function(){
    const token = crypto.randomBytes(32).toString('hex')
    this.passwordResetToken = crypto.createHash("sha256").update(token).digest('hex')
    this.passwordResetExpire = Date.now() + 10 * 60 * 1000
    
    return token
}


const User = mongoose.model('User', userSchema)

module.exports = User