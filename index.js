const Express=require('express')
const mongoose=require('mongoose')
require('dotenv').config();
const cookieSession = require("cookie-session");
const passport = require("passport");
const bodyParser=require('body-parser')
app=Express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
mongoose.connect(process.env.MONGODB_URI,{ useNewUrlParser: true,useUnifiedTopology: true })
const mdb=mongoose.connection
mdb.on('open',()=>{
    console.log("DB is connected now...")
});
app.set('view engine','ejs')
app.set('views',__dirname+'/pages')
app.use(cookieSession({
    maxAge: 24*60*60*1000,
    keys:[process.env.cookieKey]
}));
app.use(passport.initialize());
app.use(passport.session()); 
app.use(Express.static('resources'))
const auth=require('./routes/googleauth');
app.use('/auth',auth);
app.get('/login',(req,res)=>{
    res.render('login',{name:0})
})
app.get('/',(req,res)=>{
    res.render('index')
})

PORT=process.env.PORT || 3000
app.listen(PORT,()=>{console.log(`Listening on ${PORT}!`);})