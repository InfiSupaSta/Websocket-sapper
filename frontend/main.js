import {webSocket, announceThatWebSocketIsReady, webSocketOnMessage} from './websocketHandler.js';
import {messageButton, startGameButton, gameTable, messageInput, finishGameButton} from './pageElements.js';
import {sendMessageFromInputIfEnterClicked, messageButtonOnClick} from './messageHandler.js';
import {drawTable, getElementId, checkFieldInputCorrect, deleteTable} from './gameHandler.js';

webSocket.onopen = announceThatWebSocketIsReady
webSocket.onmessage = webSocketOnMessage

let gameRunning = false

messageButton.onclick = () => {
    messageButtonOnClick(webSocket)
}

startGameButton.onclick = () => {
    if (checkFieldInputCorrect()) {
        if (gameRunning === false) {
            gameRunning = true
            drawTable(webSocket)
            gameTable.addEventListener("click", getElementId)
            startGameButton.disabled = true
            finishGameButton.disabled = false
        }
    }
}

finishGameButton.onclick = () => {
    if (gameRunning === true) {
        deleteTable(gameRunning)
        startGameButton.disabled = false
        finishGameButton.disabled = true
        gameRunning = false
    }
}

messageInput.addEventListener("keydown", sendMessageFromInputIfEnterClicked)
