var button_ajax_state_sending = false;

if(!button_ajax_state_sending){ 
    function mode() {
        $.ajax({
        url: "/2d",
        type: "get",
        cache: false,
        success: function(response) {

            $('#cars').html(response);
            button_ajax_state_sending = true; // SET TRUE
            console.log('I fucking got that!');
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