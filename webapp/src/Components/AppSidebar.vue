<script setup lang="ts">
import { Link, usePage } from "@inertiajs/vue3";
import SideBarHeader from "./SideBarHeader.vue";
import SideBarFooter from "./SideBarFooter.vue";
import { SideBarMenuItems } from "@/Constants";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faChevronRight } from "@fortawesome/free-solid-svg-icons";

defineProps<{
    isOpen: boolean,
    isCollapsed?: boolean
}>();

const emit = defineEmits(['close']);

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

// Active state logic
const page = usePage();
const currentPath = computed(() => page.url ? page.url.split(/[?#]/)[0] : '');

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
        'fixed inset-y-0 left-0 z-30 bg-white dark:bg-surface-950 border-r border-surface-200 dark:border-surface-800 flex flex-col transition-all duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-auto group',
        isOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full',
        isCollapsed ? 'lg:w-20 lg:hover:w-72' : 'lg:w-72'
    ]">
        <SideBarHeader :is-collapsed="isCollapsed" />

        <div class="flex-1 overflow-y-auto px-4 py-1 custom-scrollbar">
            <ul class="flex flex-col gap-1.5">
                <li v-for="(item, index) in SideBarMenuItems" :key="index">

                    <!-- Separator -->
                    <div v-if="item.separator" class="my-3 px-2">
                        <div class="h-px bg-surface-100 dark:bg-surface-800"></div>
                    </div>

                    <!-- Item -->
                    <div v-else>
                        <div @click="item.items ? toggleExpand(item.label) : null" :class="[
                            'group flex items-center gap-3 p-2 rounded-xl cursor-pointer transition-all duration-200 select-none border border-transparent',
                            // Hover effect for the whole row
                            'hover:bg-surface-100 dark:hover:bg-surface-900',
                            (item.route && isActive(item.route)) || (item.items && isChildActive(item.items)) ? 'bg-surface-100 dark:bg-surface-900' : ''
                        ]">
                            <component :is="item.items ? 'div' : Link" :href="item.route || '#'"
                                class="flex items-center gap-3 flex-1 min-w-0">
                                <!-- Icon -->
                                <div v-if="item.icon"
                                    class="w-8 h-8 rounded-lg bg-surface-0 dark:bg-surface-800 flex items-center justify-center text-surface-500 dark:text-surface-400 group-hover:text-primary-600 dark:group-hover:text-primary-400 group-hover:bg-white dark:group-hover:bg-surface-800 shadow-sm border border-surface-200 dark:border-surface-700 transition-colors shrink-0">
                                    <font-awesome-icon :icon="item.icon" class="text-sm" />
                                </div>

                                <!-- Label -->
                                <span
                                    class="font-medium text-surface-600 dark:text-surface-300 group-hover:text-surface-900 dark:group-hover:text-surface-0 transition-colors whitespace-nowrap overflow-hidden transition-all duration-300"
                                    :class="[isCollapsed ? 'lg:w-0 lg:opacity-0 lg:group-hover:w-auto lg:group-hover:opacity-100' : 'w-auto opacity-100']">
                                    {{ item.label }}
                                </span>
                            </component>

                            <!-- Badge -->
                            <span v-if="item.badge"
                                class="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded-md transition-all duration-300"
                                :class="[
                                    'bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400 group-hover:bg-surface-200',
                                    isCollapsed ? 'lg:hidden lg:group-hover:block' : 'block'
                                ]">
                                {{ item.badge }}
                            </span>

                            <!-- Chevron -->
                            <font-awesome-icon v-if="item.items" :icon="faChevronRight" :class="[
                                'text-[10px] text-surface-400 transition-transform duration-200 ml-auto',
                                isExpanded(item.label) ? 'rotate-90' : 'rotate-0',
                                isCollapsed ? 'lg:hidden lg:group-hover:block' : 'block'
                            ]" />
                        </div>

                        <!-- Submenu -->
                        <div v-if="item.items" class="grid transition-all duration-300 ease-in-out overflow-hidden"
                            :class="[
                                isExpanded(item.label) ? 'grid-rows-[1fr] opacity-100 mt-1' : 'grid-rows-[0fr] opacity-0',
                                isCollapsed ? 'lg:hidden lg:group-hover:grid' : 'block'
                            ]">
                            <div class="overflow-hidden">

                                <!-- Tree Line Container -->
                                <ul class="flex flex-col relative pl-6">
                                    <!-- Vertical Guide Line -->
                                    <div class="absolute left-6 top-0 bottom-4 w-px bg-surface-200 dark:bg-surface-800">
                                    </div>

                                    <li v-for="(subItem, subIndex) in item.items" :key="subIndex" class="relative group/sub flex items-center ml-4  px-4 rounded-lg text-sm transition-all duration-200
                                                   
                                                   hover:bg-primary-50 dark:hover:bg-primary-900/20 
                                                   hover:text-primary-700 dark:hover:text-primary-300
                                                   
                                                   hover:translate-x-0.5" :class="[
                                                    isActive(subItem.route)
                                                        ? 'text-primary-700 dark:text-primary-300 bg-primary-50 dark:bg-primary-900/20 font-medium'
                                                        : 'text-surface-500 dark:text-surface-400'
                                                ]">

                                        <div
                                            class="absolute left-0 top-1/2 w-4 h-px bg-surface-200 dark:bg-surface-800 -translate-y-1/2">
                                        </div>

                                        <Link :href="subItem.route || '#'" class="py-2">
                                            <span>{{ subItem.label }}</span>
                                        </Link>
                                    </li>
                                </ul>

                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>

        <SideBarFooter :is-collapsed="isCollapsed" />
    </div>
</template>
