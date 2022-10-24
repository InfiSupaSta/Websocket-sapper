import {isOpen, webSocket} from './webSocketHandler.js';
import {fieldHeight, fieldWidth, finishGameButton, startGameButton} from "./pageElements.js";
import {gameTable} from './pageElements.js';
import {
    gameInitializerPrefix,
    gameMoveIdentifierPrefix,
    gameTableDeletePrefix,
    drawTableForOtherClient
} from './webSocketMessagePrefixes.js';

export function drawTable(currentWebSocket) {
    const width = fieldWidth.value
    const height = fieldHeight.value

    if (!isOpen(currentWebSocket)) return;
    if (width !== "" && height !== "") {
        const widthToInt = parseInt(width)
        const heightToInt = parseInt(height)
        const numberArray = [...Array(heightToInt).keys()]
        gameTable.innerHTML = ""
        numberArray.forEach((number) => {
            gameTable.insertAdjacentHTML("beforeend", drawTableRow(number, widthToInt))
        })

        const initMessage = gameInitializerPrefix + " " + width + " " + height
        const drawTableForOthersMessage = drawTableForOtherClient + " " + width + " " + height
        currentWebSocket.send(initMessage)
        currentWebSocket.send(drawTableForOthersMessage)
    }
}

export function drawTableRow(xPosition, elementsAmount) {

    let result = ""
    const iterationsArray = [...Array(elementsAmount).keys()]

    iterationsArray.forEach((number) => {
        const id = xPosition + "_" + number
        result += "<td id=" + id + '>' + '< >' + '</td>'
    })
    return result
}

export function getElementId(event) {
    const message = gameMoveIdentifierPrefix + " " + event.target.id
    webSocket.send(message)
    return event.target.id
}

export function colorCellToGreen(event) {
    const cellId = event.target.id
    const cellColor = document.getElementById(cellId).style.backgroundColor

    if (event.which !== 2) {
        return
    }

    if (cellColor === "") {
        document.getElementById(cellId).style.backgroundColor = "green"
    } else {
        document.getElementById(cellId).style.backgroundColor = ""
    }
}

export function checkFieldInputCorrect() {
    return fieldWidth.value !== "" && fieldHeight.value !== ""
}

export function deleteTable() {
    gameTable.innerHTML = ''
    webSocket.send(gameTableDeletePrefix)
}

export function disableStartButtonAfterGameInit() {
    startGameButton.disabled = true
    finishGameButton.disabled = false
}

export function enableStartButtonAfterGameEnd() {
    startGameButton.disabled = false
    finishGameButton.disabled = true
}