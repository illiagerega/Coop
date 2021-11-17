var map_ajax_state_sending = false;

function setCars() {
    $.ajax({
    url: "/2d",
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
            url: "/2d",
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