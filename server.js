var express = require("express"); 
var app = express(); 
var path = require("path");
var fs = require("fs")

const PORT = 6720;

if (process.argv.length === 2) {

    throw Error("No map argument provided")

}

var map_name = process.argv[process.argv.length - 1];

app.use(express.static('./public'))

fs.readdir("./public/Maps", (err, files) => {

    if (err) { throw err; }

    if (files.indexOf(map_name) > -1) {

        app.get('/',function(req,res){ 
            res.sendFile(path.join(__dirname+'./public/index.html')); 
        }); 

        app.listen(PORT);
        console.log(`Showing ${map_name} at:\nhttp://localhost:${PORT}/?map=${map_name}`)

    } else {

        console.log("No map called " + map_name);

    }

})