

export const useTheme = () => {
    const isDark = ref(false);

    const toggleTheme = () => {
        isDark.value = document.documentElement.classList.contains('dark');


        isDark.value = !isDark.value;
        if (isDark.value) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }

    return {
        isDark,
        toggleTheme
    }
}