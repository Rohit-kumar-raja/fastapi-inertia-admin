<script setup lang="ts">
import Dialog from 'primevue/dialog';

defineProps<{
    header?: string;
    width?: string;
}>();

const visible = defineModel<boolean>('visible');
</script>

<template>
    <Dialog v-model:visible="visible" modal :header="header" :style="{ width: width || '50rem' }" >
        <div class="p-6">
            <slot></slot>
        </div>

        <template #footer>
            <slot name="footer"></slot>
        </template>
    </Dialog>
</template>
