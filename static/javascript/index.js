
function sellArtwork(artworkId) {
    fetch('/sell-artwork', {
        method: 'POST',
        body: JSON.stringify({ artworkId: artworkId})
    }).then((_res) => {
        window.location.href = "/inventory";
    });
}

function buyArtwork(artworkId) {
    fetch('/buy-artwork', {
        method: 'POST',
        body: JSON.stringify({ artworkId: artworkId})
    }).then((_res) => {
        window.location.href = "/market";
    });
}

function nextDay() {
    fetch('/next-day', {
        method: 'POST',
        body: JSON.stringify({})
    }).then((_res) => {
        window.location.href = "/myAdmin";
    });
}

function genCode() {
    fetch('/gen-code', {
        method: 'POST',
        body: JSON.stringify({})
    }).then((_res) => {
        window.location.href = "/myAdmin";
    });
}


// Initialising the canvas
var canvas = document.querySelector('canvas'),
    ctx = canvas.getContext('2d');
    

// Setting the width and height of the canvas
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Setting up the letters
//var letters = 'ABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZ';
var letters = 'A B C D E F G H I J K L M N O P Q R S T U V X Y Z A B C D E F G H I J K L M N O P Q R S T U V X Y Z FUCKTHESYNS THEBANKSLIE BEFREE'
letters = letters.split(' ');

// Setting up the columns
var fontSize = 20,
    columns = canvas.width / fontSize;

// Setting up the drops
var drops = [];
for (var i = 0; i < columns; i++) {
  drops[i] = Math.floor(Math.random() * columns);
}

// Setting up the draw function
function draw() {
  
  ctx.fillStyle = 'rgba(16, 17, 17, .2)';
 
  ctx.fillRect(0, 0, canvas.width, canvas.height);


  for (var i = 0; i < drops.length; i++) {
    var chance = Math.random();
    if (chance > .98){
      var text = letters[Math.floor(Math.random() * letters.length)];
      ctx.fillStyle = '#D1153B';
      
      
      
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      
    }
    
     drops[i] = Math.floor(Math.random() * columns);
    if (drops[i] * fontSize > canvas.height && Math.random() > .95) {
      drops[i] = 0;
      
  
    }
    
  }
  
}

let isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;
ctx.fillStyle = 'rgba(16, 17, 17, 1)';
ctx.font = '20px draconic';  
ctx.fillRect(0, 0, canvas.width, canvas.height);

if (!isMobile) {
    setInterval(draw, 120);
}else{
    setInterval(draw, 120);
}
// Loop the animation


