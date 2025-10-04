const mongoose = require('mongoose')

const cartSchema = new mongoose.Schema({
    owner: {
        type: mongoose.Schema.ObjectId,
        ref: 'User'
    },
    items: [
        {
            type: mongoose.Schema.ObjectId,
            ref: 'Item'
        }
    ],
    balance: {
        type: Number,
        default: 0
    },
    level: {
        type: Number,
        default: 1
    }
})

const Cart = mongoose.model('Cart', cartSchema)

module.exports = Cart