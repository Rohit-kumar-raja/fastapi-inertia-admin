<script setup lang="ts">
import { ref } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faCog, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import { useUserStore } from '@/Store/userStore';
import Menu from 'primevue/menu';

const userStore = useUserStore();
const userMenu = ref();

const userMenuItems = ref<Array<Record<string, any>>>([
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

function toggleUserMenu(event: Event) {
    userMenu.value.toggle(event);
}
</script>

<template>
    <div class="relative">
        <button @click="toggleUserMenu"
            class="group relative flex items-center justify-center p-[2px] rounded-full transition-transform duration-200 hover:scale-105 outline-none focus:ring-2 focus:ring-primary-500/50"
            aria-label="User menu">
            <img src="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" alt="User"
                class="w-8 h-8 rounded-full object-cover border-2 border-slate-200 dark:border-white/10 group-hover:border-indigo-400 transition-colors duration-200" />
            <span
                class="absolute bottom-px right-px w-2 h-2 bg-emerald-500 rounded-full ring-2 ring-white dark:ring-surface-900"></span>
        </button>
    </div>

    <Menu ref="userMenu" :model="userMenuItems" :popup="true"
        class="border-0! shadow-xl! rounded-2xl! p-0! overflow-hidden bg-white dark:bg-slate-900 border-slate-100 dark:border-white/5 w-[200px]">
        <template #start>
            <div class="px-4 py-3 border-b border-slate-100 dark:border-white/5 bg-slate-50/50 dark:bg-white/5">
                <p class="text-sm font-semibold text-slate-800 dark:text-slate-100">Amy Elsner</p>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 truncate">amy@example.com</p>
            </div>
        </template>
        <template #item="{ item }">
            <a v-if="!item.separator"
                class="flex items-center gap-2.5 px-3.5 py-2 mx-1 my-0.5 rounded-lg text-[13px] font-medium transition-all duration-150 cursor-pointer"
                :class="[
                    item.label === 'Logout'
                        ? 'text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 hover:text-red-600 dark:hover:text-red-400'
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-white/5 hover:text-slate-900 dark:hover:text-slate-100'
                ]">
                <font-awesome-icon v-if="item.icon" :icon="item.icon" class="text-xs opacity-70" />
                <span>{{ item.label }}</span>
            </a>
        </template>
    </Menu>
</template>