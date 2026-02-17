<template>

    <div v-for="item in items" :key="item.label" class="hidden md:flex items-center gap-2 text-sm">
        <font-awesome-icon v-if="item.icon" :icon="item.icon" class="text-surface-400" />
        <span v-if="!item.to" class="text-surface-600 dark:text-surface-400">{{ item.label }}</span>
        <font-awesome-icon v-if="item.to" :icon="faChevronRight" class="text-xs text-surface-400" />
        <span v-if="item.to" class="font-semibold text-surface-900 dark:text-surface-0">{{
            item.label }}</span>
    </div>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    faHouse, faChevronRight
} from '@fortawesome/free-solid-svg-icons'

const items = ref([
    { label: 'Projects', to: '/projects', icon: faHouse },
    { label: 'Construction', to: '/construction' },
    { label: 'House Spectrum Ltd', to: '/house-spectrum-ltd' }
]);

</script>
