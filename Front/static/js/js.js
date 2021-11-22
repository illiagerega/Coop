var up = false,
    right = false,
    down = false,
    left = false,
    x = window.innerWidth/2-130/2,
    y = window.innerHeight/2-130/2
document.addEventListener('keydown',press)
function press(e){
  if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
    up = true
  }
  if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
    right = true
  }
  if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
    down = true
  }
  if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */ || e.keyCode === 81 /* q */){
    left = true
  }
}
document.addEventListener('keyup',release)
function release(e){
  if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
    up = false
  }
  if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
    right = false
  }
  if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
    down = false
  }
  if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */ || e.keyCode === 81 /* q */){
    left = false
  }
}
function gameLoop(){
  var div = document.querySelector('div')
  if (up){
    y = y - 10
  }
  if (right){
    x = x + 10
  }
  if (down){
    y = y + 10
  }
  if (left){
    x = x - 10
  }
  div.style.left = x+'px'
  div.style.top = y+'px'
  window.requestAnimationFrame(gameLoop)
}
window.requestAnimationFrame(gameLoop)

var map_ajax_state_sending = false;

function setCars() {
    $.ajax({
    url: "/map",
    type: "GET",
    data: {operation: "setCars"},
    cache: false,
    success: function(response) {
        $('#cars').html(response);
        button_ajax_state_sending = true; // SET TRUE
        console.log('I tf got that!');
        },
    
    });
    return false;
};
    

if (!map_ajax_state_sending)
{
    function setMap()
    {
        $.ajax({
            url: "/map",
            type: "get",
            data: {operation: "setMap"},
            cache: false,
            success: function(response) {
                $('#map').html(response);
                console.log(response);

                map_ajax_state_sending = true;
            },
        });
    }

}

let bool = true

const changeValue = () => {
    bool = !bool
    if (bool == false)
        setMap();
        setCars();
        
    if (bool == true)
        console.log('program has been stopped')
    console.log(bool)
}

//setMap(); // when press button start

// setInterval(mode, 2000);

var notepad = document.getElementById("car_red");
notepad.addEventListener("contextmenu",function(event){
    event.preventDefault();
    var ctxMenu = document.getElementById("ctxMenu");
    ctxMenu.style.display = "block";
    ctxMenu.style.left = (event.pageX - 10)+"px";
    ctxMenu.style.top = (event.pageY - 10)+"px";
},false);
notepad.addEventListener("click",function(event){
    var ctxMenu = document.getElementById("ctxMenu");
    ctxMenu.style.display = "";
    ctxMenu.style.left = "";
    ctxMenu.style.top = "";
},false);

