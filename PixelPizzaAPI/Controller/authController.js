const apiFeatures = require(`${__dirname}/../utils/apiFeatures`)
const User = require(`${__dirname}/../Models/userModel`)
const jwt = require('jsonwebtoken')
const AppError = require('../utils/appError')
const {promisify} = require('util')
const { updateOne, findOne } = require('../Models/userModel')
const sendEmail = require('../utils/email')
const crypto = require('crypto')

function signToken(id){
    return jwt.sign({id: id}, process.env.JWT_SECRET, {
            expiresIn: process.env.JWT_EXPIRE
        })
}
async function findUserWithJWT(headers, getPass = true){
    if(headers.authorization && headers.authorization.startsWith('Bearer')){
        token = headers.authorization.split(' ')[1]    
    }
    if(!token){
        return undefined
    }
    const decoded = await promisify(jwt.verify)(token, process.env.JWT_SECRET)
    let user;
    if(getPass){
        user = await User.findById(decoded.id).select('+password')
    }else{
        user = await User.findById(decoded.id)
    }
    return [user, decoded]
}

exports.signup = async function(req,res){
    try{
        const newUser = await User.create({
            name: req.body.name,
            email: req.body.email,
            address: req.body.address,
            passwordChangedAt: Date.now(),
            password: req.body.password,
            passwordConfirm: req.body.passwordConfirm
        })

        const token = signToken(newUser._id)
        res.status(201).json({
            status: 'success',
            token: token,
            data: newUser
        })
    }catch(err){
        console.log(err)
        res.status(400).json({
            status: 'fail',
            message: err.message
        })
    }
}
exports.login = async function(req,res, next){
    try{
        console.log(req.body)
        const {email, password} = req.body
        if(!email || !password){
            return next(new AppError('pls provide email & pass', 401))
        }
        const user = await User.findOne({email: email}).select('+password')
        if(!user || !(await user.correctPassword(password, user.password))){
            return next(new AppError('email or password is not correct'))
        } else{
            const token = signToken(user._id)
            res.cookie('jwt', token, {
                expire: new Date(Date.now() + process.env.JWT_COOKIE_EXPIRE * 24 * 60 * 60 * 1000),
                secure: false,
                httpOnly: true
            })
            return res.status(201).json({
                status: 'success',
                token
            })
        }
    }catch(err){
        res.status(400).json({
            status: 'fail',
            message: err.message
        })
    }
}

exports.updateUserLastSeen = async function(req,res,next) {
    const [user] = await findUserWithJWT(req.headers)
    console.log(user)
    user.lastSeen = new Date()
    user.save({validateBeforeSave: false})
    next()
}
exports.protect = async function(req, res, next) {
    let token;
    const [currectUser,jwt] = await findUserWithJWT(req.headers)
    if(!currectUser){
        return next(new AppError("we can't find your account, please login again or signup", 401))
    }
    if(await currectUser.changedPasswordAfter(jwt.iat)){
        return next(new AppError('the password is changed, please login again', 401))
    }
    console.log(currectUser)
    
    req.user = currectUser
    next()
}

exports.restrictTo = function(...permissions){
    return (req,res,next)=>{
        let access = []
        for (let p of req.user.permissions) {
            if(permissions.includes(p)){
                access.push(p)
            }
        }
        if(!(permissions.length===access.length)){
            return next(new AppError('you do not have permission to access', 403))
        }
        next()
    }
}

exports.forgotPassword = async function(req,res,next){
    const user = await User.findOne({email: req.body.email})
    if(!user){
        return next(new AppError("email not exists", 403))
    }
    console.log(user)
    const token = user.createResetToken()
    user.save({validateBeforeSave: false})
    console.log(5)
    const requestURL = `${req.protocol}://${req.get('host')}/resetPassword/${token}`
    const message = `click on this link to change your password:\n${requestURL}`
    try{
        await sendEmail({
            email: user.email,
            subject: 'reset password',
            message
        })
        res.status(200).json({
            status: 'success',
            message: 'sending email is successfuly!'
        })
    }catch(err){
        console.error('sending error: ' ,err)
        return next(new AppError('error in sending email', 500))

    }
    next()
}

exports.resetPassword =  async function(req,res,next) {
    const body = req.body
    const token = crypto.createHash("sha256").update(req.params.token).digest('hex')
    const user = await User.findOne({passwordResetToken: token, passwordResetExpire: {$gte: Date.now()}})
    if(!user){
        return next(new AppError('token invaild or expaired, get a new token!', 500))
    }

    user.password = body.password
    user.passwordConfirm = body.passwordConfirm
    user.passwordChangedAt = new Date()
    user.passwordResetExpire = undefined
    user.passwordResetToken = undefined

    await user.save()
    
    const JWT = signToken(user._id)
    res.status(200).json({
        status: 'success',
        token: JWT
    })
    next()
}

exports.updatePassword = async function(req,res,next) {
    const [user] = await findUserWithJWT(req.headers)
    const currectPassword = user.password
    const currectEnteredPassword = req.body.currectPassword

    if(!user || !(await user.correctPassword(currectEnteredPassword, currectPassword))){
        return next(new AppError('password or token is invaild, get a new token or enter correct password!', 403))        
    }

    await User.findByIdAndUpdate(user._id, {
        password : req.body.newPassword,
        passwordConfirm : req.body.passwordConfirm,
        passwordChangedAt : new Date()
    }, { new: true, runValidators: true })

    const token = signToken(user._id)

    res.status(200).json({
        status: 'success',
        newPassword: req.body.newPassword,
        newToken: token
    })
    next()
    }

    exports.getProfile = async function(req,res,next) {
    const [user] = await findUserWithJWT(req.headers, false)

    res.status(200).json({
        status: 'success',
        data: {name: user.name, email: user.email, address: user.address},
    })
    next()
    }

exports.updateProfile = async function(req,res,next) {
    const [user] = await findUserWithJWT(req.headers)

    await User.findByIdAndUpdate(user._id, {
        name: req.body.name || user.name,
        email: req.body.email || user.email,
        address: req.body.address || user.address
    }, { new: true, runValidators: true })

    const token = signToken(user._id)

    res.status(201).json({
        status: 'success',
        newToken: token
    })
    next()
}