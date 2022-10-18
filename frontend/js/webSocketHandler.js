import {messageContainer, gameTable} from "./pageElements.js";
import {getElementId, drawTableRow} from './gameHandler.js';
import {enableStartButtonAfterGameEnd, disableStartButtonAfterGameInit} from './gameHandler.js';
import {
    exceedConnectionsLimitPrefix,
    serverSapperResponse,
    drawTableForOtherClient,
    gameStartedPrefix,
    gameFinishedPrefix,
    gameInitializerPrefix,
    gameTableDeletePrefix
} from './webSocketMessagePrefixes';

export let webSocket = new WebSocket("ws://localhost:8765/")

export function isOpen(currentWebSocket) {
    return currentWebSocket.readyState === currentWebSocket.OPEN
}

export function webSocketOnMessage(event) {
    const message = event.data

    if (message === gameTableDeletePrefix) {
        enableStartButtonAfterGameEnd()
        gameTable.innerHTML = ''
        return
    }
    if (message === gameStartedPrefix) {
        console.log(message)
        disableStartButtonAfterGameInit()
        return
    }

    if (message.split(" ")[0] === gameInitializerPrefix) {
        disableStartButtonAfterGameInit()
        return
    }

    if (message.split(" ")[0] === serverSapperResponse) {
        console.log("Move registered!")
        const cellId = message.split(" ")[1]
        const cellInfo = message.split(" ")[2]
        document.getElementById(cellId).innerText = cellInfo

        if (cellInfo === "X") {
            document.getElementById(cellId).style.backgroundColor = "RED"
            gameTable.removeEventListener("click", getElementId)
            webSocket.send(gameFinishedPrefix)
            alert("GAME OVER!")
        }
        return
    }

    if (message.split(" ")[0] === drawTableForOtherClient) {
        const widthToInt = parseInt(message.split(" ")[1])
        const heightToInt = parseInt(message.split(" ")[2])
        const gameState = message.split(" ")[3]
        const numberArray = [...Array(heightToInt).keys()]
        gameTable.innerHTML = ""
        numberArray.forEach((number) => {
            gameTable.insertAdjacentHTML("beforeend", drawTableRow(number, widthToInt))
        })

        if (gameState === "started") {
            gameTable.addEventListener("click", getElementId)
        }

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