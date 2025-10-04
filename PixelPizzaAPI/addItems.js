const dotenv = require('dotenv')
const express = require('express')
const mongoose = require('mongoose')
const app = express()
app.use(express.json())
dotenv.config({path: `${__dirname}/config.env`})
const PORT = process.env.PORT || 3000
const DB = process.env.DB.replace('<db_password>', process.env.DB_PASSWORD)
mongoose.connect(DB).then(()=>console.log('database connection sucessful!'))
const Item = require('./Models/itemModel')
async function JSON_FILE(){
    const fetchItems = await fetch('https://raw.githubusercontent.com/YasinH4010/PixelPizza/refs/heads/master/src/Config/items.json')
    const items = await fetchItems.json()
    return items
}

async function start(){
    const items = await JSON_FILE()
    for(item of items){
        try{
            const newItem = await Item.create(item)
            console.log('ADDED: '+newItem)
        }catch(err){
            console.log('ERROR: '+err)
        }

    }

   

}
start()


app.listen(PORT, function(){
    console.log(`PixelPizzaAPI:addItems running on ${PORT}`)
})