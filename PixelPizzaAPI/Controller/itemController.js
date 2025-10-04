const { default: mongoose } = require("mongoose")
const AppError = require("../utils/appError")
const { checkItem } = require("../utils/check")

const APIFeatures = require(`${__dirname}/../utils/apiFeatures`)
const Item = require(`${__dirname}/../Models/itemModel`)

// async function checkItem(id, next) {
//     if (!mongoose.Types.ObjectId.isValid(id)) {
//       return next(new AppError('Invalid ID format', 400));
//     }
//     const item = await Item.findById(id)
//         if(!item){
//             return next(new AppError('item not found', 400))
//         }
// }

exports.getItems = async function(req,res){
    try{
        const features = new APIFeatures(Item.find(), req.query).filter().sort().fields().paginate(1000)
        const items = await features.query
        res.status(200).json({
        status: 'success',
        results: items.length,
        data: items
    })
    }catch(err){
        console.log(err)
        res.status(400).json({
            status: 'fail',
            message: err.message
        })
    }
    }

    exports.getItem = async function(req,res, next){
    try{
    const id = req.params.id
    const item = await checkItem(id, next)
        res.status(200).json({
        status: 'success',
        data: item
    })
    }catch(err){
        console.log(err)
        res.status(400).json({
            status: 'fail',
            message: err.message
        })
    }
    }


exports.deleteItem = async function(req,res, next) {
    try{
        const id = req.params.id
        await checkItem(id, next)

        await Item.findByIdAndDelete(id)
        res.status(204).end()
    }catch(e){
            return next(new AppError(e.message, 500))
    }
}

exports.editItem = async function(req,res, next) {
    try{
        const id = req.params.id
        await checkItem(id, next)

        const updatedItem = await Item.findByIdAndUpdate(id, req.body, {new: true})

        res.status(200).json({
            status: 'success',
            data: updatedItem
        })
    }catch(e){
            return next(new AppError(e.message, 500))
    }
}

exports.addItem = async function(req,res, next) {
    try{
        const newItem = await Item.create(req.body)

        res.status(200).json({
            status: 'success',
            data: newItem
        })
    }catch(e){
            return next(new AppError(e.message, 400))
    }
}


    // exports.create.
// exports.editItem = async function(req,res) {
    
// }
// exports.deleteItems = async function(req,res) {
    
// }
