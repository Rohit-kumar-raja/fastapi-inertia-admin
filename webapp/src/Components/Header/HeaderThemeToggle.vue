<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faSun, faMoon } from "@fortawesome/free-solid-svg-icons";
import { useTheme } from "@/Composables/useTheme";

const { toggleTheme, isDark } = useTheme();
</script>

<template>
    <button @click="toggleTheme"
        class="w-[34px] h-[34px] flex items-center justify-center rounded-xl text-slate-500 dark:text-slate-400 hover:text-amber-500 dark:hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-500/10 transition-all duration-200"
        aria-label="Toggle theme">
        <font-awesome-icon :icon="isDark ? faSun : faMoon" class="text-sm" />
    </button>
</template>
