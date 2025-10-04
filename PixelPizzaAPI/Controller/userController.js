const { default: mongoose } = require("mongoose");
const AppError = require("../utils/appError");
const { checkUser } = require("../utils/check");
const Cart = require("../Models/cartModel");

const APIFeatures = require(`${__dirname}/../utils/apiFeatures`)
const User = require(`${__dirname}/../Models/userModel`)


// async function checkUser(id, next) {
//     if (!mongoose.Types.ObjectId.isValid(id)) {
//       return next(new AppError('Invalid ID format', 400));
//     }
//     const user = await User.findById(id)
//         if(!user){
//             return next(new AppError('user not found', 400))
//         }
// }

exports.getUsers = async function(req,res){
    try{
        const features = new APIFeatures(User.find(), req.query).filter().sort().fields().paginate(1000)
        const users = await features.query
        res.status(200).json({
        status: 'success',
        results: users.length,
        data: users
    })
    }catch(err){
        console.log(err)
        res.status(400).json({
            status: 'fail',
            message: err.message
        })
    }
    }

    exports.getuser = async function(req,res, next){
    try{
    const id = req.params.id
    const user = await checkUser(id, next)
        res.status(200).json({
        status: 'success',
        data: user
    })
    }catch(err){
        console.log(err)
        res.status(400).json({
            status: 'fail',
            message: err.message
        })
    }
    }

exports.deleteUser = async function(req,res, next) {
    try{
        const id = req.params.id
        await checkUser(id, next)

        await User.findByIdAndDelete(id)
        res.status(204).end()
    }catch(e){
            return next(new AppError(e.message, 500))
    }
}

exports.editUser = async function(req,res,next) {
    const id = req.params.id
    const user = await checkUser(id, next)

    await User.findByIdAndUpdate(id, {
        name: req.body.name || user.name,
        email: req.body.email || user.email,
        address: req.body.address || user.address
    }, { new: true, runValidators: true })

    if(req.body.balance){
        await Cart.findByIdAndUpdate(user.cart, {
        balance: req.body.balance
    }, { new: true, runValidators: true })
    }

    const data = await User.findById(id)
    res.status(201).json({
        status: 'success',
        data
    })
    next()
}