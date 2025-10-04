const dotenv = require('dotenv')
const mongoose = require('mongoose')
const app = require('./index')
dotenv.config({path: `${__dirname}/config.env`})
const PORT = process.env.PORT || 3000
const DB = process.env.DB.replace('<db_password>', process.env.DB_PASSWORD)
mongoose.connect(DB).then(()=>console.log('database connection sucessful!'))


app.listen(PORT, function(){
    console.log(`PixelPizzaAPI running on ${PORT}`)
})