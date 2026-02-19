<script setup lang="ts">
import { Link } from "@inertiajs/vue3";
import SidebarItem from "./SidebarItem.vue";

const props = defineProps<{
    item: any;
    isCollapsed?: boolean;
    isActive?: boolean;
    isExpanded?: boolean;
    activeChildRoute?: string; // To check which child is active
}>();

const emit = defineEmits(['toggle']);

function isChildActive(route?: string) {
    if (!route || !props.activeChildRoute) return false;
    return props.activeChildRoute === route || props.activeChildRoute.startsWith(route + '/');
}
</script>

<template>
    <div>
        <!-- Group Trigger -->
        <SidebarItem :item="item" :is-collapsed="isCollapsed" :is-active="isActive" :is-expanded="isExpanded"
            :has-children="true" @click="emit('toggle')" />

        <!-- Submenu -->
        <div class="grid transition-all duration-300 ease-in-out overflow-hidden" :class="[
            isExpanded ? 'grid-rows-[1fr] opacity-100 mt-1' : 'grid-rows-[0fr] opacity-0',
            isCollapsed ? 'lg:hidden lg:group-hover:grid' : 'block'
        ]">
            <div class="overflow-hidden">
                <ul class="flex flex-col relative pl-6 pt-1">
                    <!-- Vertical Guide Line -->
                    <div class="absolute left-6 top-0 bottom-4 w-px bg-slate-200 dark:bg-slate-700"></div>

                    <li v-for="(subItem, subIndex) in item.items" :key="subIndex"
                        class="relative flex items-center ml-4 px-4 rounded-lg text-sm transition-all duration-200 hover:translate-x-0.5"
                        :class="[
                            isChildActive(subItem.route)
                                ? 'text-indigo-700 dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-500/10 font-medium'
                                : 'text-slate-500 dark:text-slate-400 hover:text-indigo-700 dark:hover:text-indigo-300 hover:bg-indigo-50 dark:hover:bg-indigo-500/10'
                        ]">

                        <!-- Horizontal connector line -->
                        <div class="absolute left-0 top-1/2 w-4 h-px bg-slate-200 dark:bg-slate-700 -translate-y-1/2">
                        </div>

                        <Link :href="subItem.route || '#'" class="py-2 flex-1 block">
                            <span>{{ subItem.label }}</span>
                        </Link>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>
