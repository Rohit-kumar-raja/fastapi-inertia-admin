<script setup lang="ts">
import AppBreadCrumb from "./AppBreadCrumb.vue";
import Notification from "./Notification.vue";
import HeaderUserMenu from "./HeaderUserMenu.vue";

import { useTheme } from "@/Composables/useTheme";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faBars, faSun, faMoon, faSearch, faExpand, faCompress,
    faTh, faHouse, faUsers, faChartBar, faFile, faCog, faFolder, faBuilding, faPlus
} from "@fortawesome/free-solid-svg-icons";
import { ref } from 'vue';
import { Link } from '@inertiajs/vue3';
import Popover from 'primevue/popover';

const emit = defineEmits(['toggle-sidebar']);
const { toggleTheme, isDark } = useTheme();

const isFullscreen = ref(false);
const searchFocused = ref(false);
const quickMenuRef = ref();

const quickActions = [
    { label: 'Dashboard', icon: faHouse, route: '/admin/dashboard', color: '#6366f1' },
    { label: 'Users', icon: faUsers, route: '/admin/administration/users', color: '#06b6d4' },
    { label: 'Roles', icon: faCog, route: '/admin/administration/roles', color: '#8b5cf6' },
    { label: 'Projects', icon: faFolder, route: '/projects/construction', color: '#f59e0b' },
    { label: 'Analytics', icon: faChartBar, route: '/analytics', color: '#10b981' },
    { label: 'Reports', icon: faFile, route: '/reports', color: '#ef4444' },
    { label: 'Companies', icon: faBuilding, route: '/companies', color: '#ec4899' },
    { label: 'People', icon: faUsers, route: '/people', color: '#14b8a6' },
];

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
        isFullscreen.value = true;
    } else {
        document.exitFullscreen();
        isFullscreen.value = false;
    }
}

function toggleQuickMenu(event: Event) {
    quickMenuRef.value.toggle(event);
}
</script>

<template>
    <header class="header-wrapper">
        <div class="header-inner">
            <!-- Left: Mobile menu + Breadcrumb -->
            <div class="flex items-center gap-2">
                <button @click="emit('toggle-sidebar')" class="lg:hidden header-icon-btn" aria-label="Toggle sidebar">
                    <font-awesome-icon :icon="faBars" class="text-base" />
                </button>

                <AppBreadCrumb />
            </div>

            <!-- Right: Actions -->
            <div class="flex items-center gap-1">
                <!-- Search Bar (Desktop) -->
                <div class="hidden md:flex items-center relative">
                    <div class="search-bar" :class="{ 'search-bar--focused': searchFocused }">
                        <font-awesome-icon :icon="faSearch" class="text-xs search-icon" />
                        <input type="text" placeholder="Search..." class="search-input" @focus="searchFocused = true"
                            @blur="searchFocused = false" />
                        <kbd class="search-kbd">⌘K</kbd>
                    </div>
                </div>

                <!-- Mobile Search -->
                <button class="md:hidden header-icon-btn" aria-label="Search">
                    <font-awesome-icon :icon="faSearch" class="text-sm" />
                </button>

                <div class="header-divider"></div>

                <!-- Quick Actions -->
                <button @click="toggleQuickMenu" class="header-icon-btn" aria-label="Quick menu">
                    <font-awesome-icon :icon="faTh" class="text-sm" />
                </button>

                <Popover ref="quickMenuRef" class="quick-menu-popover">
                    <div class="quick-menu">
                        <div class="quick-menu-header">
                            <span class="quick-menu-title">Quick Actions</span>
                        </div>
                        <div class="quick-menu-grid">
                            <Link v-for="(action, idx) in quickActions" :key="idx" :href="action.route"
                                class="quick-action-item">
                                <div class="quick-action-icon"
                                    :style="{ background: action.color + '14', color: action.color }">
                                    <font-awesome-icon :icon="action.icon" class="text-base" />
                                </div>
                                <span class="quick-action-label">{{ action.label }}</span>
                            </Link>
                        </div>
                    </div>
                </Popover>

                <!-- Fullscreen Toggle -->
                <button @click="toggleFullscreen" class="hidden sm:flex header-icon-btn" aria-label="Toggle fullscreen">
                    <font-awesome-icon :icon="isFullscreen ? faCompress : faExpand" class="text-sm" />
                </button>

                <!-- Notification -->
                <Notification />

                <!-- Theme Toggle -->
                <button @click="toggleTheme" class="header-icon-btn theme-toggle" aria-label="Toggle theme">
                    <font-awesome-icon :icon="isDark ? faSun : faMoon" class="text-sm" />
                </button>

                <div class="header-divider"></div>

                <!-- User Menu -->
                <HeaderUserMenu />
            </div>
        </div>
    </header>
</template>

<style scoped>
/* ─── Header Shell ────────────────────────────────────────────────────────── */
.header-wrapper {
    height: 56px;
    position: sticky;
    top: 0;
    z-index: 40;
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    background: rgba(255, 255, 255, 0.88);
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:root.p-dark .header-wrapper {
    background: rgba(10, 15, 30, 0.88);
    border-bottom-color: rgba(255, 255, 255, 0.06);
}

.header-inner {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
}

@media (min-width: 1024px) {
    .header-inner {
        padding: 0 24px;
    }
}

/* ─── Icon Button ─────────────────────────────────────────────────────────── */
.header-icon-btn {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    border: none;
    background: transparent;
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    outline: none;
    position: relative;
}

.header-icon-btn:hover {
    background: #f1f5f9;
    color: #334155;
    transform: translateY(-1px);
}

.header-icon-btn:active {
    transform: translateY(0);
}

:root.p-dark .header-icon-btn {
    color: #94a3b8;
}

:root.p-dark .header-icon-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #e2e8f0;
}

/* ─── Theme Toggle ────────────────────────────────────────────────────────── */
.theme-toggle:hover {
    background: rgba(251, 191, 36, 0.12);
    color: #f59e0b;
}

:root.p-dark .theme-toggle:hover {
    background: rgba(251, 191, 36, 0.15);
    color: #fbbf24;
}

/* ─── Search Bar ──────────────────────────────────────────────────────────── */
.search-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 6px 12px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    width: 200px;
}

.search-bar--focused {
    width: 280px;
    border-color: #818cf8;
    background: white;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.08);
}

:root.p-dark .search-bar {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
}

:root.p-dark .search-bar--focused {
    background: rgba(255, 255, 255, 0.08);
    border-color: #818cf8;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.search-icon {
    color: #94a3b8;
}

.search-input {
    border: none;
    outline: none;
    background: transparent;
    color: #334155;
    font-size: 13px;
    width: 100%;
    line-height: 1;
}

:root.p-dark .search-input {
    color: #e2e8f0;
}

.search-input::placeholder {
    color: #94a3b8;
    font-size: 13px;
}

.search-kbd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-family: inherit;
    font-weight: 500;
    padding: 2px 6px;
    border-radius: 5px;
    background: #f1f5f9;
    color: #94a3b8;
    border: 1px solid #e2e8f0;
    white-space: nowrap;
    line-height: 1.4;
}

:root.p-dark .search-kbd {
    background: rgba(255, 255, 255, 0.06);
    color: #64748b;
    border-color: rgba(255, 255, 255, 0.1);
}

/* ─── Divider ─────────────────────────────────────────────────────────────── */
.header-divider {
    width: 1px;
    height: 20px;
    background: #e2e8f0;
    margin: 0 6px;
}

:root.p-dark .header-divider {
    background: rgba(255, 255, 255, 0.08);
}

@media (max-width: 640px) {
    .header-divider {
        display: none;
    }
}

/* ─── Quick Menu ──────────────────────────────────────────────────────────── */
.quick-menu {
    width: 320px;
    padding: 0;
}

.quick-menu-header {
    padding: 14px 16px 10px;
    border-bottom: 1px solid #f1f5f9;
}

:root.p-dark .quick-menu-header {
    border-bottom-color: rgba(255, 255, 255, 0.06);
}

.quick-menu-title {
    font-size: 13px;
    font-weight: 600;
    color: #334155;
    letter-spacing: -0.01em;
}

:root.p-dark .quick-menu-title {
    color: #e2e8f0;
}

.quick-menu-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
    padding: 12px;
}

.quick-action-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 12px 4px;
    border-radius: 12px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
}

.quick-action-item:hover {
    background: #f8fafc;
    transform: translateY(-2px);
}

:root.p-dark .quick-action-item:hover {
    background: rgba(255, 255, 255, 0.06);
}

.quick-action-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

.quick-action-item:hover .quick-action-icon {
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.quick-action-label {
    font-size: 11px;
    font-weight: 500;
    color: #64748b;
    text-align: center;
    line-height: 1.2;
}

:root.p-dark .quick-action-label {
    color: #94a3b8;
}
</style>
