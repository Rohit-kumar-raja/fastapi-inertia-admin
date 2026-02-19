<template>
    <div class="relative">
        <button @click="toggleUserMenu" class="user-avatar-btn" aria-label="User menu">
            <img src="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" alt="User"
                class="user-avatar-img" />
            <span class="user-status-dot"></span>
        </button>
    </div>
    <Menu ref="userMenu" :model="userMenuItems" :popup="true">
        <template #start>
            <div class="user-menu-info">
                <p class="user-menu-name">Amy Elsner</p>
                <p class="user-menu-email">amy@example.com</p>
            </div>
        </template>
        <template #item="{ item }">
            <a class="user-menu-item" :class="{ 'user-menu-item--danger': item.label === 'Logout' }">
                <font-awesome-icon v-if="item.icon" :icon="item.icon" class="text-xs" />
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
        command: () => userStore.logout()
    }
]);

function toggleUserMenu(event: Event) {
    userMenu.value.toggle(event);
}
</script>

<style scoped>
.user-avatar-btn {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2px;
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: 50%;
    transition: all 0.2s ease;
    outline: none;
}

.user-avatar-btn:hover {
    transform: scale(1.05);
}

.user-avatar-img {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #e2e8f0;
    transition: border-color 0.2s ease;
}

:root.p-dark .user-avatar-img {
    border-color: rgba(255, 255, 255, 0.12);
}

.user-avatar-btn:hover .user-avatar-img {
    border-color: #818cf8;
}

.user-status-dot {
    position: absolute;
    bottom: 1px;
    right: 1px;
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    border: 2px solid white;
}

:root.p-dark .user-status-dot {
    border-color: #0a0f1e;
}

/* ─── Menu Info ────────────────────────────────────────────────────────────── */
.user-menu-info {
    padding: 12px 16px;
    border-bottom: 1px solid #f1f5f9;
}

:root.p-dark .user-menu-info {
    border-bottom-color: rgba(255, 255, 255, 0.06);
}

.user-menu-name {
    font-size: 14px;
    font-weight: 600;
    color: #1e293b;
}

:root.p-dark .user-menu-name {
    color: #f1f5f9;
}

.user-menu-email {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 2px;
}

:root.p-dark .user-menu-email {
    color: #64748b;
}

/* ─── Menu Items ───────────────────────────────────────────────────────────── */
.user-menu-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    cursor: pointer;
    border-radius: 8px;
    color: #475569;
    font-size: 13px;
    transition: all 0.15s ease;
    margin: 2px 6px;
}

.user-menu-item:hover {
    background: #f8fafc;
    color: #1e293b;
}

:root.p-dark .user-menu-item {
    color: #94a3b8;
}

:root.p-dark .user-menu-item:hover {
    background: rgba(255, 255, 255, 0.06);
    color: #f1f5f9;
}

/* Logout */
.user-menu-item--danger {
    color: #ef4444;
}

.user-menu-item--danger:hover {
    background: rgba(239, 68, 68, 0.06);
    color: #dc2626;
}

:root.p-dark .user-menu-item--danger {
    color: #f87171;
}

:root.p-dark .user-menu-item--danger:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #fca5a5;
}
</style>