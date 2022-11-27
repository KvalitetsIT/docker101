const http = require('http');
var mysql = require('mysql');
var dotenv = require('dotenv').config();

var con = mysql.createConnection({
  host: process.env.DATABASE_HOST,
  database: process.env.DATABASE_DB,
  user: process.env.DATEBASE_USER,
  password: process.env.DATABASE_PASSWORD
});


const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');

  console.log(JSON.stringify(req.headers));

  con.connect(function(err) {
    if (err) throw err;

    console.log("Connected!");
    con.query("SELECT * FROM greetings", function (err, result) {

    if (err) throw err;
      console.log("Database created");
    });
  });


  res.end('Hello World');
}).listen(8080);
