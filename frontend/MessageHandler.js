import {messageButton, messageInput, errorsInput} from './PageElements.js';

export function messageButtonOnClick(currentWebSocket) {
    const message = messageInput.value

    if (message !== "") {
        currentWebSocket.send(message)
        messageInput.value = ""
        errorsInput.value = ""
        errorsInput.innerHTML = ""

    } else {
        errorsInput.innerHTML = ""
        errorsInput.insertAdjacentText("beforeend", "MESSAGE CANT BE EMPTY!")
    }
}

export function sendMessageFromInputIfEnterClicked(event) {
    if (event.key === "Enter") {
        messageButton.onclick()
    }
}

