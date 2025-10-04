class APIFeatures{
    constructor(query,queryStr){
        this.query = query
        this.queryStr = queryStr
    }
    filter(){
        let queryObj = {...this.queryStr}
        const excaptingQuerys = ['page', 'sort', 'fields']
        excaptingQuerys.forEach(e=>delete queryObj[e])
        let queryString = JSON.stringify(queryObj)
        queryString = queryString.replace(/\b(gte|gt|lte|lt)\b/g, match=>`$${match}`)
        this.query = this.query.find(JSON.parse(queryString))
        
        return this
    }
    sort(){
        if(this.queryStr.sort){
        const sortBy = this.queryStr.sort.split(',').join(' ')
        this.query = this.query.sort(sortBy)
        
    }
    return this
}
fields(){
    if(this.queryStr.fields){
    const fields = this.queryStr.fields.split(',').join(' ')
    this.query= this.query.select(fields)
}else{
    this.query = this.query.select('-__v -password')
}
return this
}
    paginate(limit = 10){
    if(this.queryStr.page){
        const page = +this.queryStr.page || 1
        const skip = (page-1)*limit
        this.query = this.query.skip(skip).limit(limit)
    } else{
        this.query = this.query.skip(0).limit(limit)
    }
    return this
    }
}

module.exports = APIFeatures