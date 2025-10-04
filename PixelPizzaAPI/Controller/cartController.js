const mongoose = require('mongoose');
const Cart = require("../Models/cartModel")
const AppError = require("../utils/appError")
const { checkItem } = require("../utils/check");
const Order = require('../Models/orderModel');
const Counter = require('../Models/counterSchema');

async function getNextOrderID() {
  const counter = await Counter.findOneAndUpdate(
    { name: 'orderId' },
    { $inc: { seq: 1 } },
    { new: true, upsert: true }
  );
  return counter.seq;
}

async function getCartItems(cart) {
  const cartItems = await Cart.aggregate([
      { $match: { _id: new mongoose.Types.ObjectId(cart) } },
      { $unwind: '$items' },
      {
        $group: {
          _id: '$items', // item id
          quantity: { $sum: 1 },
        }
      },
      {
        $lookup: {
          from: 'items', // collection name of Item model
          localField: '_id',
          foreignField: '_id',
          as: 'itemData'
        }
      },
      { $unwind: '$itemData' },
      {
        $addFields: {
          totalPrice: { $multiply: ['$itemData.price', '$quantity'] }
        }
      },
      {
        $project: {
          _id: 0,
          item: '$itemData',
          quantity: 1,
          totalPrice: 1
        }
      }
    ]);

    return cartItems
}

exports.viewCart = async function(req, res, next) {
    try{
        const cart = await Cart.findById(req.user.cart)
        const cartItems = await getCartItems(req.user.cart)
    let totalItemsPrice = 0
    for (let index = 0; index < cartItems.length; index++) {
        totalItemsPrice += cartItems[index].totalPrice
    } 
        res.status(200).json({
            status: 'success',
            cartItems,
            totalItemsPrice,
            user: req.user,
            cart: cart
        })
    }catch(e){
        return next(new AppError(e.message, 400))
    }
}


exports.addToCart = async function(req,res, next) {
    try{
        const id = req.params.id
        await checkItem(id, next)
        const cart = await Cart.findById(req.user.cart)
        cart.items.push(id)
        await cart.save()
        res.status(201).json({
            status: 'success',
            message: `added ${id} to cart`
        })
    }catch(e){
        return next(new AppError(e.message, 400))
    }
}

exports.deleteFromCart = async function(req,res,next) {
  try{
        const id = req.params.id
        const all = req.query?.all || 'false'
        await checkItem(id, next)
        const cart = await Cart.findById(req.user.cart)
        const itemIndex = cart.items.findIndex(i=>i.toString()===id.toString())

        if (itemIndex > -1) cart.items.splice(itemIndex, 1)
        if(all==='true') cart.items = cart.items.filter(i=>i.toString()!==id.toString())
        await cart.save()

        res.status(204).end()
    }catch(e){
        return next(new AppError(e.message, 400))
    }
}

exports.checkout = async function(req,res,next) {
  try{
    const cart = await Cart.findById(req.user.cart).populate('items')
    if(!req.user.address) return next(new AppError('please first add an address to your profile', 400))
    
    let cost = 0
    for (let index = 0; index < cart.items.length; index++) {
        cost += cart.items[index].price
    }
    if(cost > cart.balance){
      return next(new AppError('Insufficient balance', 400))
    }
    const orderID = await getNextOrderID();
    const cartItems =  await getCartItems(req.user.cart)
    if(!cartItems.length){
      return next(new AppError('first, add an item', 400))
    }

    await fetch(`${process.env.TELEGRAM_BOT_API}/${orderID}`, {
  method: 'POST',
  headers: {
    'x-secret': process.env.NEW_ORDER_SECRET,
    'Content-Type': 'application/json'
  }})

    const newOrder = await Order.create({
      orderID: orderID,
      orderer: req.user._id,
      items: cartItems,
      paid: cost,
      address: req.user.address
    })

    cart.balance -= cost
    cart.items = []
    await cart.save()

    res.status(201).json({
      status: 'success',
      orderID,
      order: newOrder,
    })

  }catch(e){
        return next(new AppError(e.message, 400))
    }
}