var button_ajax_state_sending = false;

if(!button_ajax_state_sending){ 
    function mode() {
        $.ajax({
        url: "/",
        type: "get",
        cache: false,
        success: function(response) {

            $('#cars').html(response);
            button_ajax_state_sending = true; // SET TRUE

            },

            success: function(data){
                $("#cars").html(response);
                button_ajax_state_sending = false; // SET TRUE
            }
        
      });
      return false;
    };
    
}

setInterval(mode, 2000);

function moveWin(event){  
    if(event.key == 'w' || event.key == 'ц' || event.key == 'Ц'|| event.key == 'W'){
        window.scroll({
            left:window.pageXOffset,
            top:window.pageYOffset - 500,
            behavior:'smooth'
        });
        document.querySelector('.set_container').style.display = 'none';
    }if(event.key == 's' || event.key == 'ы' || event.key == 'Ы' || event.key == 'S' || event.key == 'і'|| event.key == 'І' ){
        window.scroll({
            left:window.pageXOffset,
            top:window.pageYOffset + 500,
            behavior:'smooth'
        });
        document.querySelector('.set_container').style.display = 'none';
    }if(event.key == 'a' || event.key == 'ф' || event.key == 'Ф' || event.key == 'A' ){
        window.scroll({
            top:window.pageYOffset,
            left:window.pageXOffset - 500,
            behavior:'smooth'
        });
        document.querySelector('.set_container').style.display = 'none';
    }if(event.key == 'd' || event.key == 'в' || event.key == 'В' || event.key == 'D'){
        window.scroll({
            top:window.pageYOffset,
            left:window.pageXOffset + 500,
            behavior:'smooth'
        });
        document.querySelector('.set_container').style.display = 'none';
    }
}