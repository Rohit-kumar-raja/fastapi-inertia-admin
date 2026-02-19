// Notification Service Worker
// Handles push events and notification click actions

const CACHE_NAME = 'notification-sw-v1';

// Listen for push events (for future web-push integration)
self.addEventListener('push', (event) => {
    let data = { title: 'New Notification', body: '', type: 'info', url: '/' };

    if (event.data) {
        try {
            data = { ...data, ...event.data.json() };
        } catch (e) {
            data.body = event.data.text();
        }
    }

    const typeIcons = {
        info: '📢',
        success: '✅',
        warning: '⚠️',
        error: '❌'
    };

    const options = {
        body: data.body,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        tag: data.type + '-' + Date.now(),
        data: { url: data.url || '/' },
        vibrate: [100, 50, 100],
        actions: [
            { action: 'open', title: 'Open' },
            { action: 'dismiss', title: 'Dismiss' }
        ],
        requireInteraction: false,
        silent: false,
    };

    event.waitUntil(
        self.registration.showNotification(
            `${typeIcons[data.type] || '📢'} ${data.title}`,
            options
        )
    );
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    if (event.action === 'dismiss') return;

    const url = event.notification.data?.url || '/';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
            // Focus existing tab if open
            for (const client of clientList) {
                if (client.url.includes(self.location.origin) && 'focus' in client) {
                    client.focus();
                    client.navigate(url);
                    return;
                }
            }
            // Otherwise open new tab
            if (clients.openWindow) {
                return clients.openWindow(url);
            }
        })
    );
});

// Handle messages from the main app (show notification from app context)
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SHOW_NOTIFICATION') {
        const { title, body, notificationType, url, tag } = event.data;

        const typeIcons = {
            info: '📢',
            success: '✅',
            warning: '⚠️',
            error: '❌'
        };

        self.registration.showNotification(
            `${typeIcons[notificationType] || '📢'} ${title}`,
            {
                body: body || '',
                icon: '/favicon.ico',
                badge: '/favicon.ico',
                tag: tag || 'app-notification-' + Date.now(),
                data: { url: url || '/' },
                vibrate: [100, 50, 100],
                requireInteraction: false,
            }
        );
    }
});

// Install — activate immediately
self.addEventListener('install', () => {
    self.skipWaiting();
});

// Activate — claim all clients
self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
});
