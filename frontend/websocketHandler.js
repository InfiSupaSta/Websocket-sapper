import {messageContainer, gameTable} from "./pageElements.js";
import {getElementId, drawTableRow, deleteTable, gameTableDeletePrefix} from './gameHandler.js';

export let webSocket = new WebSocket("ws://localhost:8765/")

const exceedConnectionsLimitPrefix = "__server_exceeded_limit_of_connections"
const serverSapperResponse = "__sapper_server_response_with_cell_info"
const drawTableForOtherClient = "__sapper_draw_table_for_other_clients"

export function isOpen(currentWebSocket) {
    return currentWebSocket.readyState === currentWebSocket.OPEN
}

export function webSocketOnMessage(event) {
    const message = event.data

    // need to handle it on back
    // if (message.split(" ")[0] === gameMoveIdentifierPrefix) {
    //     console.log("Game started!")
    //     return
    // }

    if (message.split(" ")[0] === serverSapperResponse) {
        console.log("Move registered!")
        const cellId = message.split(" ")[1]
        const cellInfo = message.split(" ")[2]
        document.getElementById(cellId).innerText = cellInfo

        if (cellInfo === "X") {
            document.getElementById(cellId).style.backgroundColor = "RED"
            gameTable.removeEventListener("click", getElementId)
            alert("GAME OVER!")
        }

        return
    }
    // if (message.split(" ")[0] === gameTableDeletePrefix) {
    //     deleteTable()
    //     return
    // }

    if (message.split(" ")[0] === drawTableForOtherClient) {
        const widthToInt = parseInt(message.split(" ")[1])
        const heightToInt = parseInt(message.split(" ")[2])
        const numberArray = [...Array(heightToInt).keys()]
        console.log(">>> redraw for others")
        gameTable.innerHTML = ""
        numberArray.forEach((number) => {
            gameTable.insertAdjacentHTML("beforeend", drawTableRow(number, widthToInt))
        })
        return
    }

    if (message.split(" ")[0] === exceedConnectionsLimitPrefix) {
        alert("Server is full, sorry.")
        return false;
    } else {
        messageContainer.insertAdjacentText("beforeend", message)
        messageContainer.insertAdjacentHTML("beforeend", `<br>`)
    }
}

export function announceThatWebSocketIsReady() {

    try {
        console.log("Websocket connection is ready!")
    } catch (error) {
        console.log(error.data)
    }
}