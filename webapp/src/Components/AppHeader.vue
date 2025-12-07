<script setup lang="ts">
import Button from "primevue/button";
import Badge from "primevue/badge";
import Popover from "primevue/popover";
import Menu from "primevue/menu";
import Avatar from "primevue/avatar";
import { ref, onMounted } from "vue";
import AppBreadCrumb from "./AppBreadCrumb.vue";

const isDark = ref(false);
const emit = defineEmits(['toggle-sidebar']);

const notificationPanel = ref();
const userMenu = ref();

const notifications = ref([
    { id: 1, title: 'New message from John', time: '5 min ago', icon: 'envelope', read: false },
    { id: 2, title: 'Project deadline approaching', time: '1 hour ago', icon: 'calendar', read: false },
    { id: 3, title: 'Task completed successfully', time: '2 hours ago', icon: 'check-circle', read: true }
]);

const userMenuItems = ref([
    {
        label: 'Profile',
        icon: 'user',
        command: () => console.log('Profile')
    },
    {
        label: 'Settings',
        icon: 'cog',
        command: () => console.log('Settings')
    },
    {
        separator: true
    },
    {
        label: 'Logout',
        icon: 'sign-out',
        command: () => console.log('Logout')
    }
]);

const unreadCount = ref(notifications.value.filter(n => !n.read).length);

onMounted(() => {
    // Check if dark mode is already enabled
    isDark.value = document.documentElement.classList.contains('dark');
});

function toggleTheme() {
    isDark.value = !isDark.value;
    if (isDark.value) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    }
}

function toggleNotifications(event: Event) {
    notificationPanel.value.toggle(event);
}

function toggleUserMenu(event: Event) {
    userMenu.value.toggle(event);
}

function markAsRead(id: number) {
    const notification = notifications.value.find(n => n.id === id);
    if (notification) {
        notification.read = true;
        unreadCount.value = notifications.value.filter(n => !n.read).length;
    }
}
</script>

<template>
    <header
        class="h-16 bg-white dark:bg-surface-900 border-b border-surface-200 dark:border-surface-700 flex items-center justify-between px-4 lg:px-6 transition-colors duration-300">
        <div class="flex items-center gap-3 text-surface-500">
            <Button text rounded severity="secondary" aria-label="Menu"
                class="lg:hidden w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800"
                @click="emit('toggle-sidebar')">
                <font-awesome-icon :icon="['fas', 'bars']" class="text-lg" />
            </Button>



            <AppBreadCrumb />
        </div>

        <div class="flex items-center gap-2">
            <Button text severity="secondary" size="small"
                class="hidden lg:flex gap-2 hover:bg-surface-100 dark:hover:bg-surface-800">
                <font-awesome-icon :icon="['fas', 'sliders-h']" />
                <span>Manage</span>
            </Button>

            <Button text severity="secondary" size="small"
                class="hidden lg:flex gap-2 hover:bg-surface-100 dark:hover:bg-surface-800">
                <font-awesome-icon :icon="['fas', 'share-alt']" />
                <span>Share</span>
            </Button>

            <Button text rounded severity="secondary" aria-label="More"
                class="hidden sm:flex w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                <font-awesome-icon :icon="['fas', 'ellipsis-h']" />
            </Button>

            <div class="w-px h-6 bg-surface-200 dark:bg-surface-700 mx-2 hidden sm:block"></div>

            <!-- Notification Button -->
            <div class="relative">
                <Button text rounded severity="secondary" @click="toggleNotifications" aria-label="Notifications"
                    class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800 relative">
                    <font-awesome-icon :icon="['fas', 'bell']" class="text-lg" />
                </Button>
                <Badge v-if="unreadCount > 0" :value="unreadCount" severity="danger" size="small"
                    class="absolute top-0 right-0 w-[1px] h-[1px] p-0 flex items-center justify-center text-[1px]" />
            </div>

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
                                    class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center flex-shrink-0">
                                    <font-awesome-icon :icon="['fas', notification.icon]"
                                        class="text-primary-600 dark:text-primary-400" />
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-surface-900 dark:text-surface-0">{{
                                        notification.title }}</p>
                                    <p class="text-xs text-surface-500 mt-1">{{ notification.time }}</p>
                                </div>
                                <div v-if="!notification.read"
                                    class="w-2 h-2 rounded-full bg-primary-500 flex-shrink-0 mt-2"></div>
                            </div>
                        </div>
                    </div>
                    <Button label="View All Notifications" text class="mt-3 w-full justify-center" size="small" />
                </div>
            </Popover>

            <!-- Theme Toggle -->
            <Button text rounded severity="secondary" @click="toggleTheme" aria-label="Toggle theme"
                class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                <font-awesome-icon :icon="['fas', isDark ? 'sun' : 'moon']" class="text-lg" />
            </Button>

            <!-- User Menu -->
            <div class="relative">
                <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle"
                    class="cursor-pointer ring-2 ring-surface-200 dark:ring-surface-700 hover:ring-primary-500 transition-all"
                    @click="toggleUserMenu" />
            </div>

            <Menu ref="userMenu" :model="userMenuItems" :popup="true">
                <template #item="{ item }">
                    <a
                        class="flex items-center gap-3 px-3 py-2 cursor-pointer hover:bg-surface-100 dark:hover:bg-surface-800 rounded transition-colors">
                        <font-awesome-icon v-if="item.icon" :icon="['fas', item.icon]" class="text-surface-400" />
                        <span>{{ item.label }}</span>
                    </a>
                </template>
            </Menu>
        </div>
    </header>
</template>
