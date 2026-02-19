import { ref, onMounted } from 'vue';

const isDark = ref(false);

export const useTheme = () => {

    // Initialize state from DOM or localStorage on first use/mount
    function initTheme() {
        const storedTheme = localStorage.getItem('theme');
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (storedTheme === 'dark' || (!storedTheme && systemDark)) {
            document.documentElement.classList.add('dark');
            isDark.value = true;
        } else {
            document.documentElement.classList.remove('dark');
            isDark.value = false;
        }
    }

    const toggleTheme = () => {
        isDark.value = !isDark.value;
        if (isDark.value) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }

    // Ensure we sync with current state when composable is used
    onMounted(() => {
        // If the class is already there (maybe from a script in head), sync ref
        if (document.documentElement.classList.contains('dark')) {
            isDark.value = true;
        } else {
            // Otherwise try to init from storage
            initTheme();
        }
    });

    return {
        isDark,
        toggleTheme
    }
}