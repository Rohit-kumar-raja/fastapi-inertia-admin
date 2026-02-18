<template>
    <div class="relative">
        <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle"
            class="cursor-pointer ring-2 ring-surface-200 dark:ring-surface-700 hover:ring-primary-500 transition-all"
            @click="toggleUserMenu" />
    </div>
    <Menu ref="userMenu" :model="userMenuItems" :popup="true">
        <template #item="{ item }">
            <a
                class="flex items-center gap-3 px-3 py-2 cursor-pointer hover:bg-surface-100 dark:hover:bg-surface-800 rounded transition-colors" :class="{'text-red-500!':item.label=='Logout'}">
                <font-awesome-icon v-if="item.icon" :icon="item.icon" class="text-surface-400" :class="{'text-red-500!':item.label=='Logout'}" />
                <span>{{ item.label }}</span>
            </a>
        </template>
    </Menu>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faCog, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import { useUserStore } from '@/Store/userStore';
const userStore = useUserStore()
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
        class: 'text-red-500',
        command: () => userStore.logout()
    }
]);




function toggleUserMenu(event: Event) {
    userMenu.value.toggle(event);
}
</script>