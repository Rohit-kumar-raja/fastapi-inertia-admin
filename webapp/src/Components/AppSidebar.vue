<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { usePage } from "@inertiajs/vue3";
import SideBarHeader from "./Sidebar/SidebarHeader.vue";
import SideBarFooter from "./Sidebar/SidebarFooter.vue";
import SidebarItem from "./Sidebar/SidebarItem.vue";
import SidebarGroup from "./Sidebar/SidebarGroup.vue";
import { SideBarMenuItems } from "@/Constants";

defineProps<{
    isOpen: boolean,
    isCollapsed?: boolean
}>();

const emit = defineEmits(['close']);

// ─── State ───────────────────────────────────────────────────────────────────
const expandedItems = ref<string[]>(['']);

function toggleExpand(label: string) {
    const index = expandedItems.value.indexOf(label);
    if (index === -1) {
        expandedItems.value.push(label);
    } else {
        expandedItems.value.splice(index, 1);
    }
}

function isExpanded(label: string) {
    return expandedItems.value.includes(label);
}

const page = usePage();
const currentPath = computed(() => new URL(page.url, window.location.origin).pathname);

function isActive(route?: string) {
    if (!route || !currentPath.value) return false;
    return currentPath.value === route || currentPath.value.startsWith(route + '/');
}

function isChildActive(children: any[]) {
    return children.some(child => isActive(child.route));
}

// Auto-expand groups with active children and keep them in sync with URL
watch(currentPath, () => {
    SideBarMenuItems.value.forEach(item => {
        if (item.items && isChildActive(item.items)) {
            if (!expandedItems.value.includes(item.label)) {
                expandedItems.value.push(item.label);
            }
        }
    });
}, { immediate: true });
</script>

<template>
    <div :class="[
        'fixed inset-y-0 left-0 z-30 bg-white dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800 flex flex-col transition-all duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-auto group',
        isOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full',
        isCollapsed ? 'lg:w-20 lg:hover:w-72' : 'lg:w-72'
    ]">

        <SideBarHeader :is-collapsed="isCollapsed" />

        <div class="flex-1 overflow-y-auto px-4 py-3 custom-scrollbar">
            <ul class="flex flex-col gap-1.5">
                <li v-for="(item, index) in SideBarMenuItems" :key="index">

                    <!-- Separator -->
                    <div v-if="item.separator" class="my-2 px-2">
                        <div class="h-px bg-slate-100 dark:bg-slate-800"></div>
                    </div>

                    <!-- Group (Submenu) -->
                    <SidebarGroup v-else-if="item.items" :item="item" :is-collapsed="isCollapsed"
                        :is-active="isChildActive(item.items)" :is-expanded="isExpanded(item.label)"
                        :active-child-route="currentPath" @toggle="toggleExpand(item.label)" />

                    <!-- Single Item -->
                    <SidebarItem v-else :item="item" :is-collapsed="isCollapsed" :is-active="isActive(item.route)" />
                </li>
            </ul>
        </div>

        <SideBarFooter :is-collapsed="isCollapsed" />
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
    background: rgba(156, 163, 175, 0.5);
    border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: rgba(107, 114, 128, 0.8);
}
</style>
