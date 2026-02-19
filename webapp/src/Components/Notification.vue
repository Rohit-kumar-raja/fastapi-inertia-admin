<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faBell, faInfoCircle, faCheckCircle, faExclamationTriangle, faTimesCircle,
    faTimes, faCheck, faCheckDouble, faTrash, faInbox
} from "@fortawesome/free-solid-svg-icons";
import Button from 'primevue/button';
import Popover from 'primevue/popover';
import axios from 'axios';
import { admin } from '@/core';

// ─── Types ───────────────────────────────────────────────────────────────────
interface Notification {
    id: string;
    title: string;
    message: string;
    type: 'info' | 'success' | 'warning' | 'error';
    is_read: boolean;
    created_at: string;
}

// ─── State ───────────────────────────────────────────────────────────────────
const notificationPanel = ref();
const notifications = ref<Notification[]>([]);
const unreadCount = ref(0);
const loading = ref(false);
let pollInterval: ReturnType<typeof setInterval> | null = null;
let pushPermission = ref<NotificationPermission>('default');

// ─── Type Config ─────────────────────────────────────────────────────────────
const typeConfig = {
    info: {
        icon: faInfoCircle,
        bg: 'bg-blue-50 dark:bg-blue-900/20',
        iconColor: 'text-blue-500 dark:text-blue-400',
        ring: 'ring-blue-100 dark:ring-blue-900/30',
        iconBg: 'bg-blue-100 dark:bg-blue-900/40',
    },
    success: {
        icon: faCheckCircle,
        bg: 'bg-emerald-50 dark:bg-emerald-900/20',
        iconColor: 'text-emerald-500 dark:text-emerald-400',
        ring: 'ring-emerald-100 dark:ring-emerald-900/30',
        iconBg: 'bg-emerald-100 dark:bg-emerald-900/40',
    },
    warning: {
        icon: faExclamationTriangle,
        bg: 'bg-amber-50 dark:bg-amber-900/20',
        iconColor: 'text-amber-500 dark:text-amber-400',
        ring: 'ring-amber-100 dark:ring-amber-900/30',
        iconBg: 'bg-amber-100 dark:bg-amber-900/40',
    },
    error: {
        icon: faTimesCircle,
        bg: 'bg-red-50 dark:bg-red-900/20',
        iconColor: 'text-red-500 dark:text-red-400',
        ring: 'ring-red-100 dark:ring-red-900/30',
        iconBg: 'bg-red-100 dark:bg-red-900/40',
    },
};

// ─── Time Helpers ────────────────────────────────────────────────────────────
function timeAgo(dateStr: string): string {
    const now = new Date();
    const date = new Date(dateStr);
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function isToday(dateStr: string): boolean {
    const date = new Date(dateStr);
    const today = new Date();
    return date.toDateString() === today.toDateString();
}

const todayNotifications = computed(() =>
    notifications.value.filter(n => isToday(n.created_at))
);
const earlierNotifications = computed(() =>
    notifications.value.filter(n => !isToday(n.created_at))
);

// ─── API Calls ───────────────────────────────────────────────────────────────
async function fetchNotifications() {
    try {
        const res = await axios.get(admin.NOTIFICATIONS_API);
        const oldCount = unreadCount.value;
        notifications.value = res.data.data || [];

        // Count unread
        const newUnread = notifications.value.filter(n => !n.is_read).length;
        unreadCount.value = newUnread;

        // Browser push for new notifications
        if (newUnread > oldCount && oldCount > 0) {
            const newest = notifications.value.find(n => !n.is_read);
            if (newest) sendBrowserPush(newest);
        }
    } catch (e) {
        console.error('Failed to fetch notifications:', e);
    }
}

async function fetchUnreadCount() {
    try {
        const res = await axios.get(admin.NOTIFICATIONS_COUNT_API);
        const newCount = res.data.data?.count ?? 0;

        // If count increased, refetch full list to get the new notification for push
        if (newCount > unreadCount.value && unreadCount.value > 0) {
            await fetchNotifications();
            return;
        }
        unreadCount.value = newCount;
    } catch (e) {
        console.error('Failed to fetch count:', e);
    }
}

async function markAsRead(id: string) {
    try {
        await axios.put(`${admin.NOTIFICATIONS_API}/${id}/read`);
        const n = notifications.value.find(n => n.id === id);
        if (n) {
            n.is_read = true;
            unreadCount.value = Math.max(0, unreadCount.value - 1);
        }
    } catch (e) {
        console.error('Failed to mark as read:', e);
    }
}

async function markAllRead() {
    try {
        await axios.put(admin.NOTIFICATIONS_READ_ALL_API);
        notifications.value.forEach(n => (n.is_read = true));
        unreadCount.value = 0;
    } catch (e) {
        console.error('Failed to mark all as read:', e);
    }
}

async function deleteNotification(id: string, event: Event) {
    event.stopPropagation();
    try {
        await axios.delete(`${admin.NOTIFICATIONS_API}/${id}`);
        const idx = notifications.value.findIndex(n => n.id === id);
        if (idx !== -1) {
            if (!notifications.value[idx].is_read) {
                unreadCount.value = Math.max(0, unreadCount.value - 1);
            }
            notifications.value.splice(idx, 1);
        }
    } catch (e) {
        console.error('Failed to delete notification:', e);
    }
}

// ─── Browser Push Notifications ──────────────────────────────────────────────
async function requestPushPermission() {
    if (!('Notification' in window)) return;
    pushPermission.value = Notification.permission;
    if (Notification.permission === 'default') {
        const result = await Notification.requestPermission();
        pushPermission.value = result;
    }
}

function sendBrowserPush(notification: Notification) {
    if (!('Notification' in window) || Notification.permission !== 'granted') return;
    const typeLabels: Record<string, string> = {
        info: 'ℹ️', success: '✅', warning: '⚠️', error: '❌'
    };
    new window.Notification(notification.title, {
        body: notification.message || undefined,
        icon: '/favicon.ico',
        tag: notification.id,
        badge: typeLabels[notification.type] || 'ℹ️',
    });
}

// ─── Toggle ──────────────────────────────────────────────────────────────────
function toggleNotifications(event: Event) {
    notificationPanel.value.toggle(event);
    if (!notifications.value.length) fetchNotifications();
}

// ─── Lifecycle ───────────────────────────────────────────────────────────────
onMounted(() => {
    fetchNotifications();
    requestPushPermission();
    // Poll for new notifications every 30s
    pollInterval = setInterval(fetchUnreadCount, 30000);
});

onUnmounted(() => {
    if (pollInterval) clearInterval(pollInterval);
});
</script>

<template>
    <div class="relative">
        <!-- Bell Button -->
        <Button text rounded severity="secondary" @click="toggleNotifications" aria-label="Notifications"
            class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800 relative">
            <font-awesome-icon :icon="faBell" class="text-lg" />
        </Button>

        <!-- Badge -->
        <span v-if="unreadCount > 0"
            class="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 flex items-center justify-center text-[10px] font-bold text-white bg-red-500 rounded-full ring-2 ring-white dark:ring-surface-900 animate-pulse">
            {{ unreadCount > 99 ? '99+' : unreadCount }}
        </span>

        <!-- Dropdown Panel -->
        <Popover ref="notificationPanel" class="w-96">
            <div class="flex flex-col max-h-[480px]">

                <!-- Header -->
                <div
                    class="flex items-center justify-between px-4 py-3 border-b border-surface-200 dark:border-surface-800">
                    <div class="flex items-center gap-2">
                        <h3 class="font-semibold text-surface-900 dark:text-surface-0 text-sm">Notifications</h3>
                        <span v-if="unreadCount > 0"
                            class="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300">
                            {{ unreadCount }} new
                        </span>
                    </div>
                    <Button v-if="unreadCount > 0" @click="markAllRead" text size="small"
                        class="text-xs text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg px-2 py-1">
                        <font-awesome-icon :icon="faCheckDouble" class="mr-1" />
                        Mark all read
                    </Button>
                </div>

                <!-- Scrollable Body -->
                <div class="overflow-y-auto flex-1 custom-scrollbar">

                    <!-- Empty State -->
                    <div v-if="notifications.length === 0 && !loading"
                        class="flex flex-col items-center justify-center py-12 px-4">
                        <div
                            class="w-16 h-16 rounded-2xl bg-surface-100 dark:bg-surface-800 flex items-center justify-center mb-4">
                            <font-awesome-icon :icon="faInbox" class="text-2xl text-surface-400" />
                        </div>
                        <p class="text-sm font-medium text-surface-500 dark:text-surface-400">No notifications yet</p>
                        <p class="text-xs text-surface-400 dark:text-surface-500 mt-1">We'll notify you when something
                            arrives</p>
                    </div>

                    <!-- Today Group -->
                    <div v-if="todayNotifications.length > 0">
                        <div class="px-4 py-2 bg-surface-50/80 dark:bg-surface-900/50 sticky top-0 z-10">
                            <span
                                class="text-[11px] font-semibold uppercase tracking-wider text-surface-400">Today</span>
                        </div>
                        <div class="px-2 py-1">
                            <div v-for="n in todayNotifications" :key="n.id" @click="!n.is_read && markAsRead(n.id)"
                                :class="[
                                    'flex items-start gap-3 px-3 py-3 rounded-xl cursor-pointer transition-all duration-200 group/item relative',
                                    n.is_read
                                        ? 'hover:bg-surface-50 dark:hover:bg-surface-900'
                                        : `${typeConfig[n.type]?.bg || ''} hover:ring-1 ${typeConfig[n.type]?.ring || ''}`
                                ]">
                                <!-- Type Icon -->
                                <div :class="[
                                    'w-9 h-9 rounded-xl flex items-center justify-center shrink-0 mt-0.5',
                                    n.is_read
                                        ? 'bg-surface-100 dark:bg-surface-800'
                                        : typeConfig[n.type]?.iconBg || 'bg-surface-100'
                                ]">
                                    <font-awesome-icon :icon="typeConfig[n.type]?.icon || faInfoCircle" :class="[
                                        'text-sm',
                                        n.is_read
                                            ? 'text-surface-400'
                                            : typeConfig[n.type]?.iconColor || 'text-surface-500'
                                    ]" />
                                </div>

                                <!-- Content -->
                                <div class="flex-1 min-w-0">
                                    <p :class="[
                                        'text-[13px] leading-snug',
                                        n.is_read
                                            ? 'text-surface-500 dark:text-surface-400'
                                            : 'text-surface-900 dark:text-surface-0 font-medium'
                                    ]">
                                        {{ n.title }}
                                    </p>
                                    <p v-if="n.message"
                                        class="text-xs text-surface-400 dark:text-surface-500 mt-0.5 line-clamp-2">
                                        {{ n.message }}
                                    </p>
                                    <p class="text-[11px] text-surface-400 mt-1">{{ timeAgo(n.created_at) }}</p>
                                </div>

                                <!-- Actions -->
                                <div
                                    class="flex items-center gap-1 opacity-0 group-hover/item:opacity-100 transition-opacity shrink-0">
                                    <button v-if="!n.is_read" @click.stop="markAsRead(n.id)"
                                        class="w-7 h-7 rounded-lg flex items-center justify-center text-surface-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
                                        title="Mark as read">
                                        <font-awesome-icon :icon="faCheck" class="text-xs" />
                                    </button>
                                    <button @click="deleteNotification(n.id, $event)"
                                        class="w-7 h-7 rounded-lg flex items-center justify-center text-surface-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                                        title="Delete">
                                        <font-awesome-icon :icon="faTrash" class="text-xs" />
                                    </button>
                                </div>

                                <!-- Unread Dot -->
                                <span v-if="!n.is_read"
                                    class="absolute top-3 right-3 w-2 h-2 rounded-full bg-primary-500 ring-2 ring-primary-500/20 group-hover/item:hidden">
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Earlier Group -->
                    <div v-if="earlierNotifications.length > 0">
                        <div class="px-4 py-2 bg-surface-50/80 dark:bg-surface-900/50 sticky top-0 z-10">
                            <span
                                class="text-[11px] font-semibold uppercase tracking-wider text-surface-400">Earlier</span>
                        </div>
                        <div class="px-2 py-1">
                            <div v-for="n in earlierNotifications" :key="n.id" @click="!n.is_read && markAsRead(n.id)"
                                :class="[
                                    'flex items-start gap-3 px-3 py-3 rounded-xl cursor-pointer transition-all duration-200 group/item relative',
                                    n.is_read
                                        ? 'hover:bg-surface-50 dark:hover:bg-surface-900'
                                        : `${typeConfig[n.type]?.bg || ''} hover:ring-1 ${typeConfig[n.type]?.ring || ''}`
                                ]">
                                <!-- Type Icon -->
                                <div :class="[
                                    'w-9 h-9 rounded-xl flex items-center justify-center shrink-0 mt-0.5',
                                    n.is_read
                                        ? 'bg-surface-100 dark:bg-surface-800'
                                        : typeConfig[n.type]?.iconBg || 'bg-surface-100'
                                ]">
                                    <font-awesome-icon :icon="typeConfig[n.type]?.icon || faInfoCircle" :class="[
                                        'text-sm',
                                        n.is_read
                                            ? 'text-surface-400'
                                            : typeConfig[n.type]?.iconColor || 'text-surface-500'
                                    ]" />
                                </div>

                                <!-- Content -->
                                <div class="flex-1 min-w-0">
                                    <p :class="[
                                        'text-[13px] leading-snug',
                                        n.is_read
                                            ? 'text-surface-500 dark:text-surface-400'
                                            : 'text-surface-900 dark:text-surface-0 font-medium'
                                    ]">
                                        {{ n.title }}
                                    </p>
                                    <p v-if="n.message"
                                        class="text-xs text-surface-400 dark:text-surface-500 mt-0.5 line-clamp-2">
                                        {{ n.message }}
                                    </p>
                                    <p class="text-[11px] text-surface-400 mt-1">{{ timeAgo(n.created_at) }}</p>
                                </div>

                                <!-- Actions -->
                                <div
                                    class="flex items-center gap-1 opacity-0 group-hover/item:opacity-100 transition-opacity shrink-0">
                                    <button v-if="!n.is_read" @click.stop="markAsRead(n.id)"
                                        class="w-7 h-7 rounded-lg flex items-center justify-center text-surface-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
                                        title="Mark as read">
                                        <font-awesome-icon :icon="faCheck" class="text-xs" />
                                    </button>
                                    <button @click="deleteNotification(n.id, $event)"
                                        class="w-7 h-7 rounded-lg flex items-center justify-center text-surface-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                                        title="Delete">
                                        <font-awesome-icon :icon="faTrash" class="text-xs" />
                                    </button>
                                </div>

                                <!-- Unread Dot -->
                                <span v-if="!n.is_read"
                                    class="absolute top-3 right-3 w-2 h-2 rounded-full bg-primary-500 ring-2 ring-primary-500/20 group-hover/item:hidden">
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Push Permission Banner -->
                <div v-if="pushPermission === 'default'"
                    class="px-4 py-2.5 border-t border-surface-200 dark:border-surface-800 bg-gradient-to-r from-primary-50 to-primary-100/50 dark:from-primary-900/20 dark:to-primary-800/10">
                    <div class="flex items-center justify-between">
                        <p class="text-xs text-primary-700 dark:text-primary-300">Enable browser notifications?</p>
                        <Button @click="requestPushPermission" size="small" severity="secondary"
                            class="text-xs px-2.5 py-1 rounded-lg">
                            Enable
                        </Button>
                    </div>
                </div>
            </div>
        </Popover>
    </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}
</style>
