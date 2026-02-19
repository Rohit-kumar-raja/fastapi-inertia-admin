import { ref } from 'vue';
import axios from 'axios';
import { admin } from '@/core';

const swRegistration = ref<ServiceWorkerRegistration | null>(null);
const pushPermission = ref<NotificationPermission>('default');
const isSupported = ref(false);
const isSubscribed = ref(false);

let initialized = false;

/**
 * Composable for managing Service Worker–based browser push notifications
 * with VAPID server-side Web Push support.
 */
export function useNotificationPush() {

    async function init() {
        if (initialized) return;
        initialized = true;

        isSupported.value = 'serviceWorker' in navigator && 'Notification' in window && 'PushManager' in window;
        if (!isSupported.value) return;

        pushPermission.value = Notification.permission;

        try {
            const reg = await navigator.serviceWorker.register('/sw.js', { scope: '/' });
            swRegistration.value = reg;

            // Check if already subscribed
            const existingSub = await reg.pushManager.getSubscription();
            isSubscribed.value = !!existingSub;

            console.log('[SW] Registered:', reg.scope, existingSub ? '(subscribed)' : '(not subscribed)');
        } catch (err) {
            console.error('[SW] Registration failed:', err);
        }
    }

    async function requestPermission(): Promise<NotificationPermission> {
        if (!isSupported.value) return 'denied';

        const result = await Notification.requestPermission();
        pushPermission.value = result;

        // If granted, automatically subscribe to server push
        if (result === 'granted' && !isSubscribed.value) {
            await subscribeToPush();
        }

        return result;
    }

    /**
     * Subscribe to server-side Web Push:
     * 1. Get VAPID public key from backend
     * 2. Subscribe via PushManager
     * 3. Send subscription to backend
     */
    async function subscribeToPush() {
        if (!swRegistration.value) return;

        try {
            // 1. Get VAPID public key from server
            const res = await axios.get(`${admin.NOTIFICATIONS_API}/vapid-public-key`);
            const vapidPublicKey = res.data.data?.publicKey;
            if (!vapidPublicKey) {
                console.warn('[Push] No VAPID public key configured on server');
                return;
            }

            // 2. Convert VAPID key to Uint8Array
            const applicationServerKey = urlBase64ToUint8Array(vapidPublicKey);

            // 3. Subscribe via PushManager
            const subscription = await swRegistration.value.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: applicationServerKey as BufferSource,
            });

            // 4. Send subscription to backend
            const subJson = subscription.toJSON();
            await axios.post(`${admin.NOTIFICATIONS_API}/push/subscribe`, {
                endpoint: subJson.endpoint,
                keys: {
                    p256dh: subJson.keys?.p256dh || '',
                    auth: subJson.keys?.auth || '',
                },
            });

            isSubscribed.value = true;
            console.log('[Push] Subscribed successfully');
        } catch (err) {
            console.error('[Push] Subscription failed:', err);
        }
    }

    /**
     * Unsubscribe from server push.
     */
    async function unsubscribeFromPush() {
        if (!swRegistration.value) return;

        try {
            const subscription = await swRegistration.value.pushManager.getSubscription();
            if (subscription) {
                // Notify backend
                const subJson = subscription.toJSON();
                await axios.post(`${admin.NOTIFICATIONS_API}/push/unsubscribe`, {
                    endpoint: subJson.endpoint,
                    keys: {
                        p256dh: subJson.keys?.p256dh || '',
                        auth: subJson.keys?.auth || '',
                    },
                });

                // Unsubscribe locally
                await subscription.unsubscribe();
                isSubscribed.value = false;
                console.log('[Push] Unsubscribed');
            }
        } catch (err) {
            console.error('[Push] Unsubscribe failed:', err);
        }
    }

    /**
     * Show a local notification via the service worker (fallback for non-push).
     */
    function showNotification(opts: {
        title: string;
        body?: string;
        type?: 'info' | 'success' | 'warning' | 'error';
        url?: string;
        tag?: string;
    }) {
        if (pushPermission.value !== 'granted') return;

        // Use service worker if available (works even when tab is in background)
        if (swRegistration.value?.active) {
            swRegistration.value.active.postMessage({
                type: 'SHOW_NOTIFICATION',
                title: opts.title,
                body: opts.body || '',
                notificationType: opts.type || 'info',
                url: opts.url || '/',
                tag: opts.tag,
            });
            return;
        }

        // Fallback to basic Notification API
        const typeIcons: Record<string, string> = {
            info: '📢', success: '✅', warning: '⚠️', error: '❌'
        };
        new Notification(`${typeIcons[opts.type || 'info']} ${opts.title}`, {
            body: opts.body || undefined,
            icon: '/favicon.ico',
            tag: opts.tag,
        });
    }

    return {
        init,
        requestPermission,
        subscribeToPush,
        unsubscribeFromPush,
        showNotification,
        pushPermission,
        isSupported,
        isSubscribed,
        swRegistration,
    };
}


/**
 * Convert a base64url-encoded string to a Uint8Array (for applicationServerKey).
 */
function urlBase64ToUint8Array(base64String: string): Uint8Array {
    const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; i++) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}
