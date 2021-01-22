
function hide_image(id, laps){

window.timerID =  setInterval(function() {
var aOpaque = document.getElementById('imageID').style.opacity;
aOpaque = aOpaque-.1;

aOpaque = aOpaque.toFixed(1);

document.getElementById(id).style.opacity = aOpaque;

if(document.getElementById(id).style.opacity<=0) clearInterval(window.timerID);
}, laps);
}





