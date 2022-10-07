import {webSocket, announceThatWebSocketIsReady, webSocketOnMessage} from './WebsocketHandler.js';
import {messageButton} from './PageElements.js';
import {sendMessageFromInputIfEnterClicked, messageButtonOnClick} from './MessageHandler.js';

webSocket.onopen = announceThatWebSocketIsReady
webSocket.onmessage = webSocketOnMessage

messageButton.onclick = () => {
    messageButtonOnClick(webSocket)
}

addEventListener("keydown", sendMessageFromInputIfEnterClicked)