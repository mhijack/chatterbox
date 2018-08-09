document.addEventListener('DOMContentLoaded', () => {
    // COnnect to websocket
    const socket = io.connect(
        `${location.protocol}//${document.domain}:${location.port}`
    );

    // When socket is connected, configure behaviors
    socket.on('connect', () => {
        document.querySelector('.create').addEventListener('click', () => {
            const room_name = document.querySelector('.room_name').value;

            if (room_name) {
                socket.emit('create room', {
                    name: room_name
                });
            } else {
				alert('Please enter a name for the channel.');
            }
        });
    });

    socket.on('room created', data => {
        document
            .querySelector('.channel_list_ul')
            .insertAdjacentHTML(
                'beforeEnd',
                `<li><a href="/channel/${data.name}">${data.name}</a></li>`
            );

        document.querySelector('.room_name').value = '';
    });
});
