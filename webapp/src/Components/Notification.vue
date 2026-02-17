<script setup lang="ts">
import { ref, computed } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faBell, faEnvelope, faCalendar, faCheckCircle
} from "@fortawesome/free-solid-svg-icons";
import Button from 'primevue/button';
import Badge from 'primevue/badge';
import Popover from 'primevue/popover';

const notificationPanel = ref();

const notifications = ref([
    { id: 1, title: 'New message from John', time: '5 min ago', icon: faEnvelope, read: false },
    { id: 2, title: 'Project deadline approaching', time: '1 hour ago', icon: faCalendar, read: false },
    { id: 3, title: 'Task completed successfully', time: '2 hours ago', icon: faCheckCircle, read: true }
]);

const unreadCount = computed(() => notifications.value.filter(n => !n.read).length);

function toggleNotifications(event: Event) {
    notificationPanel.value.toggle(event);
}

function markAsRead(id: number) {
    const notification = notifications.value.find(n => n.id === id);
    if (notification) {
        notification.read = true;
    }
}
</script>

<template>
    <div class="relative">
        <Button text rounded severity="secondary" @click="toggleNotifications" aria-label="Notifications"
            class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800 relative">
            <font-awesome-icon :icon="faBell" class="text-lg" />
        </Button>
        <Badge v-if="unreadCount > 0" :value="unreadCount" severity="danger" size="small"
            class="absolute top-0 right-0 w-px h-px p-0 flex items-center justify-center text-[1px]" />

        <Popover ref="notificationPanel" class="w-80">
            <div class="flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="font-semibold text-surface-900 dark:text-surface-0">Notifications</h3>
                    <Button label="Mark all as read" text size="small" class="text-xs" />
                </div>
                <div class="flex flex-col gap-2 max-h-96 overflow-y-auto">
                    <div v-for="notification in notifications" :key="notification.id"
                        @click="markAsRead(notification.id)" :class="[
                            'p-3 rounded-lg cursor-pointer transition-colors',
                            notification.read ? 'bg-surface-50 dark:bg-surface-800' : 'bg-primary-50 dark:bg-primary-900/20'
                        ]">
                        <div class="flex items-start gap-3">
                            <div
                                class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center shrink-0">
                                <font-awesome-icon :icon="notification.icon"
                                    class="text-primary-600 dark:text-primary-400" />
                            </div>
                            <div class="flex-1 min-w-0">
                                <p class="text-sm font-medium text-surface-900 dark:text-surface-0">{{
                                    notification.title }}</p>
                                <p class="text-xs text-surface-500 mt-1">{{ notification.time }}</p>
                            </div>
                            <div v-if="!notification.read" class="w-2 h-2 rounded-full bg-primary-500 shrink-0 mt-2">
                            </div>
                        </div>
                    </div>
                </div>
                <Button label="View All Notifications" text class="mt-3 w-full justify-center" size="small" />
            </div>
        </Popover>
    </div>
</template>
