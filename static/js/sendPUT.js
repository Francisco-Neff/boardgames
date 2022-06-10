function sendPUT() {
    var frm = $('#modPerfil');
    var data = {
        id_username: $("#id_username").val(),
        id_email: $("#id_email").val()
    };
    console.log(data)
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "X-Requested-With": "XMLHttpRequest"
        },
        contentType: 'application/json',
        data: JSON.stringify(data), 
    success: function () {  
            location.reload();
        },
    error: function () {   
        console.log('FAIL');
        alert('No se ha actualizado tu perfil.')
        $("#id_username").val('')
        $("#id_email").val('')
        }
    });
}