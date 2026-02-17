<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import Menu from 'primevue/menu';
import Avatar from 'primevue/avatar';
import AppBreadCrumb from "./AppBreadCrumb.vue";
import Notification from "./Notification.vue";

import { useUserStore } from "@/Store/userStore";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faBars, faSlidersH, faShareAlt, faEllipsisH,
    faSun, faMoon, faUser, faCog, faSignOutAlt
} from "@fortawesome/free-solid-svg-icons";

const isDark = ref(false);
const emit = defineEmits(['toggle-sidebar']);
const userStore = useUserStore();

const userMenu = ref();

const userMenuItems = ref<any>([
    {
        label: 'Profile',
        icon: faUser,
        command: () => console.log('Profile')
    },
    {
        label: 'Settings',
        icon: faCog,
        command: () => console.log('Settings')
    },
    {
        separator: true
    },
    {
        label: 'Logout',
        icon: faSignOutAlt,
        command: () => userStore.logout()
    }
]);

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

function toggleUserMenu(event: Event) {
    userMenu.value.toggle(event);
}
</script>

<template>
    <header
        class="h-16 bg-white dark:bg-surface-900 border-b border-surface-200 dark:border-surface-700 flex items-center justify-between px-4 lg:px-6 transition-colors duration-300">
        <div class="flex items-center gap-3 text-surface-500">
            <Button text rounded severity="secondary" aria-label="Menu"
                class="lg:hidden w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800"
                @click="emit('toggle-sidebar')">
                <font-awesome-icon :icon="faBars" class="text-lg" />
            </Button>



            <AppBreadCrumb />
        </div>

        <div class="flex items-center gap-2">
            <Button text severity="secondary" size="small"
                class="hidden lg:flex hover:bg-surface-100 dark:hover:bg-surface-800" label="Manage">
                <template #icon>
                    <font-awesome-icon :icon="faSlidersH" />
                </template>
            </Button>

            <Button text severity="secondary" size="small"
                class="hidden lg:flex hover:bg-surface-100 dark:hover:bg-surface-800" label="Share">
                <template #icon>
                    <font-awesome-icon :icon="faShareAlt" />
                </template>
            </Button>

            <Button text rounded severity="secondary" aria-label="More"
                class="hidden sm:flex w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                <font-awesome-icon :icon="faEllipsisH" />
            </Button>

            <div class="w-px h-6 bg-surface-200 dark:bg-surface-700 mx-2 hidden sm:block"></div>

            <!-- Notification Button -->
            <Notification />


            <!-- Theme Toggle -->
            <Button text rounded severity="secondary" @click="toggleTheme" aria-label="Toggle theme"
                class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                <font-awesome-icon :icon="isDark ? faSun : faMoon" class="text-lg" />
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
                        <font-awesome-icon v-if="item.icon" :icon="item.icon" class="text-surface-400" />
                        <span>{{ item.label }}</span>
                    </a>
                </template>
            </Menu>
        </div>
    </header>
</template>
