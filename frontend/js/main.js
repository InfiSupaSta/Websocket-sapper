import {webSocket, announceThatWebSocketIsReady, webSocketOnMessage} from './webSocketHandler.js';
import {messageButton, startGameButton, gameTable, messageInput, finishGameButton} from './pageElements.js';
import {sendMessageFromInputIfEnterClicked, messageButtonOnClick} from './messageHandler.js';
import {
    drawTable,
    getElementId,
    checkFieldInputCorrect,
    deleteTable,
    enableStartButtonAfterGameEnd,
    colorCellToGreen
} from './gameHandler.js';

webSocket.onopen = announceThatWebSocketIsReady
webSocket.onmessage = webSocketOnMessage


messageButton.onclick = () => {
    messageButtonOnClick(webSocket)
}

startGameButton.onclick = () => {
    if (checkFieldInputCorrect()) {
        drawTable(webSocket)
        gameTable.addEventListener("click", getElementId)

        startGameButton.disabled = true
        finishGameButton.disabled = false
    }
}

finishGameButton.onclick = () => {
    let answer = window.confirm("Are you sure?")
    if (answer) {
        deleteTable()
        enableStartButtonAfterGameEnd()
    }
}

messageInput.addEventListener("keydown", sendMessageFromInputIfEnterClicked)
gameTable.addEventListener("mousedown", colorCellToGreen)