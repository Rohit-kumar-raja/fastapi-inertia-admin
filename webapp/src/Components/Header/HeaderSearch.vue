<script setup lang="ts">
import { ref } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faSearch } from "@fortawesome/free-solid-svg-icons";

const searchFocused = ref(false);
</script>

<template>
    <!-- Desktop Search -->
    <div class="hidden md:flex items-center relative">
        <div class="flex items-center gap-2 bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-xl px-3 py-1.5 transition-all duration-200 ease-in-out w-[200px]"
            :class="{ 'w-[280px] bg-white dark:bg-white/10 border-indigo-400 dark:border-indigo-500 ring-4 ring-indigo-500/10 dark:ring-indigo-400/10': searchFocused }">
            <font-awesome-icon :icon="faSearch" class="text-xs text-slate-400" />
            <input type="text" placeholder="Search..."
                class="bg-transparent border-none outline-none text-[13px] w-full text-slate-700 dark:text-slate-200 placeholder-slate-400"
                @focus="searchFocused = true" @blur="searchFocused = false" />
            <kbd
                class="inline-flex items-center justify-center text-[10px] font-medium px-1.5 py-0.5 rounded bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-slate-400 whitespace-nowrap leading-tight">⌘K</kbd>
        </div>
    </div>

    <!-- Mobile Search Button -->
    <button
        class="md:hidden w-[34px] h-[34px] flex items-center justify-center rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/10 hover:text-slate-700 dark:hover:text-slate-200 transition-all duration-200"
        aria-label="Search">
        <font-awesome-icon :icon="faSearch" class="text-sm" />
    </button>
</template>
