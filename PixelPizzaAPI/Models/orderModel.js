const { default: mongoose } = require("mongoose");

const ORDER_STATUSES = [
  'checking',
  'preparing',
  'baking',
  'out_for_delivery',
  'delivered',
  'cancelled'
];

const orderSchema = mongoose.Schema({
    orderID: {
        type: Number,
        required: true,
        unique: true
    },
    orderer: {
        type: mongoose.Schema.ObjectId,
        ref: 'User'
    },
    items: [Object],
    paid: {
        type: Number,
        required: true,
    },
    address: {
        type: String,
        required: true,
    },
    status: {
    type: String,
    enum: ORDER_STATUSES,
    default: 'checking',
    required: true,
    index: true
  }
}, { timestamps: true })

const Order = mongoose.model('Order', orderSchema)

module.exports = Order