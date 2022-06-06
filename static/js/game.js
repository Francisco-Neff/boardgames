var sala_cod = document.getElementById("tablero").getAttribute("sala");
var ficha = document.getElementById("tablero").getAttribute("ficha");
var jugador = document.getElementById("head").getAttribute("username");
var id_game = null
var ws_url_String = 'ws://' + window.location.host + '/ttt/partida/' + sala_cod + '/';
var gameSocket = new WebSocket(ws_url_String);
var ganador = ''
var fichas_X = []
var fichas_O = []
var tablero = [
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
];
ganadorIndices = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
let movimientos = 0;
let turno = true;

let celdas = document.getElementsByClassName('celda');
for (var i = 0; i < celdas.length; i++){
    celdas[i].addEventListener("click", event=>{
        const index = event.path[0].getAttribute('data-index');
        if(tablero[index] == -1){
            if(!turno){
                alert("Espera tu turno")
            }
            else{
                turno = false;
                document.getElementById("turno").style.display = 'none'; // Hide          
                make_move(index, ficha);
            }
        }
    })
}

function make_move(index, ficha){
    index = parseInt(index);
    let data = {
        "evento": "MOVE",
        "mensaje": {
            "id_game":id_game,
            "index": index,
            "ficha": ficha
        }
    }
    console.log('move')
    
    if(tablero[index] == -1){
        movimientos++;
        if(ficha == 'X') {
            tablero[index] = 1;
            var celda = document.querySelector('[data-index="'+index+'"]');
            celda.classList.add('ficha_X');
            localStorage.setItem(index,'X')
        }
        else if(ficha == 'O'){
            tablero[index] = 0;
            var celda = document.querySelector('[data-index="'+index+'"]');
            celda.classList.add('ficha_O');
            localStorage.setItem(index,'O')
        }
        else{
            alert("Se ha ingresado un valor no valido.");
            return false;
        }
        //almacenar_movimientos(index,ficha)
        gameSocket.send(JSON.stringify(data))
    }
    celdas[index].innerHTML = ficha;
    ganador = comprobarGanador();
    if(turno){
        if(ganador){
            data = {
                "evento": "END",
                "mensaje": {
                    "id_game":id_game,
                    "index": index,
                    "ficha": ficha, //revisar esto.
                    "final": jugador,
                    "alert": `${ficha} es el ganador. Jugar de nuevo?`
                }
            }
            console.log('end con ganador')
            gameSocket.send(JSON.stringify(data))
        }
        else if(!ganador && movimientos == 9){
            data = {
                "evento": "END",
                "mensaje": {
                    "id_game":id_game,
                    "index": index,
                    "ficha": ficha, //revisar esto.
                    "final": 'T',
                    "alert" : "Empate. Jugar de nuevo?"
                }
            }
            console.log('end sin ganador')
            gameSocket.send(JSON.stringify(data))
        }
    }
}

function reset(){
    tablero = [
        -1, -1, -1,
        -1, -1, -1,
        -1, -1, -1,
    ]; 
    movimientos = 0;
    turno = true;
    document.getElementById("turno").style.display = 'inline';        
    for (var i = 0; i < celdas.length; i++){
        celdas[i].innerHTML = "";
    }
}

const check = (ganadorIndex) => {
    if (
      tablero[ganadorIndex[0]] !== -1 &&
      tablero[ganadorIndex[0]] === tablero[ganadorIndex[1]] &&
      tablero[ganadorIndex[0]] === tablero[ganadorIndex[2]]
    )   return true;
    return false;
};

function comprobarGanador(){
    let ganador = false;
    if (movimientos >= 5) {
      ganadorIndices.forEach((w) => {
        if (check(w)) {
          ganador = true;
          ganadorIndice = w;
        }
      });
    }
    return ganador;
}


function connect() {
    gameSocket.onopen = function open() {
        console.log('Conexión creada correctamente.');
        gameSocket.send(JSON.stringify({
            "evento": "START",
            "mensaje": {
                "sala": sala_cod,
                "jugador":jugador,
                "ficha": ficha
            }
        }));
    };

    gameSocket.onclose = function (e) {
        console.log('Socket cerrado. Relanzando conexión en 1 seg.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };
    // Sending the info about the room
    gameSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        id = data['id_game']
        data = data["respuesta"];
        let mensaje = data['mensaje'];
        let evento = data["evento"];
        switch (evento) {
            case "START":
                id_game=id
                console.log('startin',id_game)
                //crear un nuevo registro en BBDD
                //verficar que no hay una partida a medias
                reset();
                
                break;
            case "END":
                alert(mensaje['alert']);
                reset();
                gameSocket.send(JSON.stringify({
                    "evento": "START",
                    "mensaje": {
                        "sala": sala_cod,
                        "jugador":jugador,
                        "ficha": ficha
                    }
                }));
                break;
            case "MOVE":
                if(mensaje["ficha"] != ficha){
                    make_move(mensaje["index"], mensaje["ficha"])
                    turno = true;
                    document.getElementById("turno").style.display = 'inline';        
                }
                break;
            case "RELOAD":
                // TODO meter un recarga del tablero
                console.log('RELOAD')
                console.log(mensaje)
                break;
            default:
                console.log("Evento no reconocido")
        }
    };

    if (gameSocket.readyState == WebSocket.OPEN) {
        gameSocket.onopen();
    }
}

connect();
