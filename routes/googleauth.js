const auth=require('express').Router();
const passport = require("passport");
const User=require('../models/User');

const GoogleStrategy = require("passport-google-oauth20").Strategy;

passport.use(
    new GoogleStrategy(
      {
        clientID: process.env.clientID,
        clientSecret: process.env.clientSecret,
        callbackURL: "/auth/google/redirect"
      },async (accessToken, refreshToken, profile, done) => {

        const search=await User.find({googleID:profile.id})
        
        if(search.length===0){
          const wow = new User({
                    googleID: profile.id,
                    name: profile.displayName,
                    email: profile.emails[0].value
                  })
          wow.save();
          // const created=await User.find({name:profile.displayName})
          
          done(null, wow);
        }else{
        
          done(null, search[0]);
        }
    })
      
  ); 

class Login {
    check=0;
}

let main=new Login;
auth.get('/',(req,res)=>{
    res.send('auth route!!')
});

auth.get("/google", passport.authenticate("google", {
    scope: ["profile", "email"]
}));

auth.get("/google/redirect",passport.authenticate("google"),(req,res)=>{
    main.check=1;
    res.redirect('/auth/portfolio')
});

auth.get("/logout", (req, res) => {
    res.render('login',{name:req.user.name})
    main.check=0;
});



auth.get('/portfolio',(req,res)=>{
  if(main.check!== 0){
    res.render('portfolio',{username:req.user.name,email:req.user.email})
  }else{ 
    res.send("Not allowed to enter :(")
  }
})


passport.serializeUser((user, done) => {
  done(null, user._id);
});

passport.deserializeUser(async (id, done) => {
  User.findById(id).then(user => {
    done(null, user);
    
  });
  
});
module.exports=auth