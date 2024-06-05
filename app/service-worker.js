self.addEventListener('push', function(event) {
    let data = {};
    if (event.data) {
        data = event.data.json();
    }

    const options = {
        body: data.body,
        icon: data.icon,
        image: data.image
    };

    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});
