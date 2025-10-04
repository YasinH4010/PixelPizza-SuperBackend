const Order = require("../Models/orderModel")
const AppError = require("../utils/appError")
const APIFeatures = require(`${__dirname}/../utils/apiFeatures`)

exports.getOrders = async function(req,res){
    try{
        const features = new APIFeatures(Order.find(), req.query).filter().sort().fields().paginate(20)
        const orders = await features.query
        res.status(200).json({
        status: 'success',
        results: orders.length,
        data: orders
    })
    }catch(err){
        console.log(err)
        res.status(400).json({
            status: 'fail',
            message: err.message
        })
    }
    }

exports.viewOrder = async function(req,res,next) {
    try{
        const order = await Order.findOne({orderID: req.params.id})
        if(!order) return next(new AppError('order not found', 400))
        if(req.user._id.toString() !== order.orderer.toString()) return next(new AppError('you can\'t access to this order', 403))
        res.status(200).json({
            status: 'success',
            data: order
        })
    }catch(e){
            return next(new AppError(e.message, 400))
    }
}

exports.manageOrder = async function(req,res,next) {
    try{
        const order = await Order.findOne({orderID: req.params.id})
        if(!order) return next(new AppError('order not found', 400))
        res.status(200).json({
            status: 'success',
            data: order
        })
    }catch(e){
            return next(new AppError(e.message, 400))
    }
}

exports.editOrder = async function(req,res,next) {
    try{
        const order = await Order.findOne({orderID: req.params.id})
        if(!order) return next(new AppError('order not found', 400))
            
        await Order.findByIdAndUpdate(order._id, {
        status : req.body.status || order.status,
        address : req.body.address || order.address
    }, { new: true, runValidators: true })

        await order.save()
        res.status(201).json({
            status: 'success',
            data: order
        })
    }catch(e){
            return next(new AppError(e.message, 400))
    }
}

