import {messageContainer} from "./PageElements.js";

export let webSocket = new WebSocket("ws://localhost:8765/")

export function webSocketOnMessage (event) {
    const message = event.data
    messageContainer.insertAdjacentText("beforeend", message)
    messageContainer.insertAdjacentHTML("beforeend", `<br>`)
}

export function announceThatWebSocketIsReady() {
    try {
        console.log("Websocket connection is ready!")
    } catch (error) {
        console.log(error.data)
    }
}