const WebSocket = require('ws');

const WebSocketServer = WebSocket.Server;

// 实例化:
const wss = new WebSocketServer({
    port: 3000
});

// 如果有WebSocket请求接入，wss对象可以响应connection事件来处理这个WebSocket：
wss.on('connection', function (ws) {
    console.log(`[SERVER] connection()`);
    // 通过响应message事件，在收到消息后再返回一个ECHO: xxx的消息给客户端。
    ws.on('message', function (message) {
        console.log(`[SERVER] Received: ${message}`);
        setTimeout(() => {
            ws.send(`What's your name?`, (err) => {
                if (err) {
                    console.log(`[SERVER] error: ${err}`);
                }
            });
        }, 1000);
    })
});

console.log('ws server started at port 3000...');

// client test:

let count = 0;

let ws = new WebSocket('ws://localhost:3000/ws/chat');

ws.on('open', function () {
    console.log(`[CLIENT] open()`);
    ws.send('Hello!');
});

ws.on('message', function (message) {
    console.log(`[CLIENT] Received: ${message}`);
    count++;
    if (count > 3) {
        ws.send('Goodbye!');
        ws.close();
    } else {
        setTimeout(() => {
            ws.send(`Hello, I'm Mr No.${count}!`);
        }, 1000);
    }
});

// 补充:
// the back-tick allows you to use string templating for example:
/*
var value = 4;
var str = `text with a ${value}`
// str will be  : 'text with a 4'
*/
