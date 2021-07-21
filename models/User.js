mongoose=require('mongoose')

const Schema=mongoose.Schema({
    googleID:{
        type:String,
    },
    name:{
        type: String
    },
    email:{
        type:String,
        requred:true
    },
    quantity:{
        type:Number
    },
    buying:{
        type:Number
    },
    current:{
        type:Number
    }
});

module.exports=mongoose.model('Algo:)',Schema);