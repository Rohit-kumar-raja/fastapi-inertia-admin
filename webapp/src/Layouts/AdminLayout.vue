<script setup lang="ts">
import AppSidebar from "@/Components/AppSidebar.vue";
import AppHeader from "@/Components/AppHeader.vue";
import { ref } from "vue";
import AppFooter from "@/Components/AppFooter.vue";

const isMobileSidebarOpen = ref(false);
const isDesktopSidebarCollapsed = ref(false);

function toggleSidebar() {
    if (window.innerWidth >= 1024) { // lg breakpoint
        isDesktopSidebarCollapsed.value = !isDesktopSidebarCollapsed.value;
    } else {
        isMobileSidebarOpen.value = !isMobileSidebarOpen.value;
    }
}
</script>

<template>
    <div class="flex h-screen bg-surface-100 dark:bg-surface-950 transition-colors duration-300 overflow-hidden">
        <!-- Backdrop -->
        <div v-if="isMobileSidebarOpen" class="fixed inset-0 bg-black/50 z-20 lg:hidden"
            @click="isMobileSidebarOpen = false"></div>

        <AppSidebar :is-open="isMobileSidebarOpen" :is-collapsed="isDesktopSidebarCollapsed"
            @close="isMobileSidebarOpen = false" />

        <div class="flex-1 flex flex-col min-w-0">
            <AppHeader @toggle-sidebar="toggleSidebar" />
            <main class="flex-1 overflow-y-auto p-1">
                <slot />
            </main>
            <AppFooter/>
        </div>
    </div>
</template>
