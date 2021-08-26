var express = require("express"); 
var app = express(); 
var path = require("path");
var fs = require("fs")

const PORT = 6720; // Port to run on

if (process.argv.length < 3) { // Checks if min arguments are defined

    throw Error("No map argument provided")

}

var map_name = process.argv[2]; // gets name of map argument

var version = process.argv[3] === "3D" ? "&version=3D" : "&version=2D"; // Get map mode from arguments

app.use(express.static('./public')) // get public folder redy for serving

fs.readdir("./public/Maps", (err, files) => {

    if (err) { throw err; }

    if (files.indexOf(map_name) > -1) { // Checks if map exists

        app.get('/', (req,res) => { 

            res.sendFile(path.join(__dirname+'./public/index.html'));  // Server index.html
            
        }); 

        app.listen(PORT); // Run on port
        console.log(`Showing ${map_name} at:\nhttp://localhost:${PORT}/?map=${map_name}` + version) // Give website name with arguments

    } else { // No map exists by that name

        console.log("No map called " + map_name);

    }

})