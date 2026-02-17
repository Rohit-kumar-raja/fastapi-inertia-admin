<script setup lang="ts">
import { computed } from 'vue';
import { usePage, Link } from '@inertiajs/vue3';
import { SideBarMenuItems } from '@/Constants';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faChevronRight, faHouse } from '@fortawesome/free-solid-svg-icons';

const page = usePage();

const breadcrumbs = computed(() => {
    let currentPath = '';
    try {
        // Safe parsing of both partial and relative URLs
        const urlObj = new URL(page.url, 'http://localhost');
        currentPath = urlObj.pathname;
    } catch {
        // Fallback or handle as relative path directly
        currentPath = page.url ? page.url.split(/[?#]/)[0] : '';
    }

    // DFS to find the longest matching route in the sidebar
    let bestMatchChain: any[] = [];
    let longestMatchLen = -1;

    function search(items: any[], chain: any[]) {
        for (const item of items) {
            const currentChain = [...chain, item];

            // Check if this item matches the current path
            if (item.route) {
                const isExact = currentPath === item.route;
                const isParent = currentPath.startsWith(item.route + '/');

                if ((isExact || isParent) && item.route.length > longestMatchLen) {
                    longestMatchLen = item.route.length;
                    bestMatchChain = currentChain;
                }
            }

            if (item.items) {
                search(item.items, currentChain);
            }
        }
    }

    search(SideBarMenuItems.value, []);

    const crumbs = [...bestMatchChain];

    // Determine the remaining path segments not covered by the sidebar match
    let matchedPath = '';
    if (bestMatchChain.length > 0) {
        // The last item in the chain typically corresponds to the matched route
        const lastMatched = bestMatchChain[bestMatchChain.length - 1];
        matchedPath = lastMatched.route || '';
    }

    // Careful with slice if matchedPath is empty
    const remaining = currentPath.slice(matchedPath.length);
    const segments = remaining.split('/').filter(p => p);

    let accumulatedPath = matchedPath;
    segments.forEach(segment => {
        // Handle root slash
        const separator = accumulatedPath.endsWith('/') ? '' : '/';
        accumulatedPath = accumulatedPath + separator + segment;

        // Basic formatting for segments
        const label = segment.charAt(0).toUpperCase() + segment.slice(1).replace(/-/g, ' ');
        crumbs.push({
            label: label,
            route: accumulatedPath,
        });
    });

    // If we have no crumbs, or the first crumb isn't Dashboard/Home, insert Home
    if (crumbs.length === 0 || (crumbs[0].label !== 'Dashboard' && crumbs[0].label !== 'Home')) {
        crumbs.unshift({
            label: '',
            route: '/dashboard',
            icon: faHouse
        });
    }

    return crumbs;
});
</script>

<template>
    <div class="hidden md:flex items-center gap-2 text-sm">
        <template v-for="(item, index) in breadcrumbs" :key="index">
            <font-awesome-icon v-if="index > 0" :icon="faChevronRight" class="text-xs text-surface-400" />

            <component :is="(item.route && index < breadcrumbs.length - 1) ? Link : 'span'" :href="item.route" :class="[
                (item.route && index < breadcrumbs.length - 1)
                    ? 'text-surface-600 dark:text-surface-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors'
                    : 'font-semibold text-surface-900 dark:text-surface-0'
            ]">
                <font-awesome-icon v-if="item.icon" :icon="item.icon" class="mr-1 " />
                <span class="px-1">{{ item.label }}</span>
            </component>
        </template>
    </div>
</template>
