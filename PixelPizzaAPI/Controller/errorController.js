exports.globalError = function(err,req,res,next){
    err.statusCode = err.statusCode || 500
    res.status(err.statusCode).json({
        status: err.status,
        message: err.message
    })
    next(err)
}