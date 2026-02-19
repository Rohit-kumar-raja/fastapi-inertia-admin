<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faExpand, faCompress } from "@fortawesome/free-solid-svg-icons";
import { useFullscreen } from '@/Composables/useFullscreen';

const { isFullscreen, toggleFullscreen } = useFullscreen();
</script>

<template>
    <button @click="toggleFullscreen"
        class="hidden sm:flex w-[34px] h-[34px] items-center justify-center rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/10 hover:text-slate-700 dark:hover:text-slate-200 transition-all duration-200"
        aria-label="Toggle fullscreen">
        <font-awesome-icon :icon="isFullscreen ? faCompress : faExpand" class="text-sm" />
    </button>
</template>
