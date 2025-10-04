const { default: mongoose } = require("mongoose");
const User = require("../Models/userModel");
const AppError = require("./appError");
const Item = require(`${__dirname}/../Models/itemModel`)

exports.checkItem = async function(id, next) {
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return next(new AppError('Invalid ID format', 400))
    }
    const item = await Item.findById(id)
        if(!item){
            return next(new AppError('item not found', 400))
        }
        return item
}

exports.checkUser = async function(id, next) {
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return next(new AppError('Invalid ID format', 400))
    }
    const user = await User.findById(id)
        if(!user){
            return next(new AppError('user not found', 400))
        }
        return user
}
