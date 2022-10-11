import {isOpen, webSocket} from './websocketHandler.js';
import {fieldHeight, fieldWidth} from "./pageElements.js";
import {gameTable} from './pageElements.js';

export const gameInitializerPrefix = "__sapper_init_field_size"
export const gameMoveIdentifierPrefix = "__sapper_cell_clicked"
export const gameTableDeletePrefix = "__sapper_game_table_delete"
const drawTableForOtherClient = "__sapper_draw_table_for_other_clients"

export function drawTable(currentWebSocket) {
    const width = fieldWidth.value
    const height = fieldHeight.value

    if (!isOpen(currentWebSocket)) return;
    if (width !== "" && height !== "") {
        // start drawing
        const widthToInt = parseInt(width)
        const heightToInt = parseInt(height)
        const numberArray = [...Array(heightToInt).keys()]
        gameTable.innerHTML = ""
        numberArray.forEach((number) => {
            gameTable.insertAdjacentHTML("beforeend", drawTableRow(number, widthToInt))
        })
        // end drawing

        const initMessage = gameInitializerPrefix + " " + width + " " + height
        const drawTable_forOthersMessage = drawTableForOtherClient + " " + width + " " + height
        currentWebSocket.send(initMessage)
        currentWebSocket.send(drawTable_forOthersMessage)
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
    // console.log(event.target.id)
    const message = gameMoveIdentifierPrefix + " " + event.target.id
    console.log(message)
    webSocket.send(message)
    return event.target.id
}

export function checkFieldInputCorrect() {
    return fieldWidth.value !== "" && fieldHeight.value !== ""
}

export function deleteTable(gameStartState) {
    let answer = window.confirm("Are you sure?")
    if (answer && gameStartState === true) {
        gameTable.innerHTML = ''
        webSocket.send(gameTableDeletePrefix)
    }
}