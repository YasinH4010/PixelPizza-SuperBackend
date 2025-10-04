const mongoose = require('mongoose')

const itemSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'required error'],
        unique: [true, 'unique error']
    },
    image: {
        type: String,
        required: [true, 'required error'],
    },
    price: {
        type: Number,
        required: [true, 'required error'],
    },
    weight: {
        type: String,
        required: [true, 'required error'],
    },
    category: {
        type: String,
        required: [true, 'required error'],
    }
})

const Item = mongoose.model('Item', itemSchema)

module.exports = Item