import { ref, onMounted, onUnmounted } from 'vue';

export function useFullscreen() {
    const isFullscreen = ref(false);

    function toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    function updateState() {
        isFullscreen.value = !!document.fullscreenElement;
    }

    onMounted(() => {
        document.addEventListener('fullscreenchange', updateState);
    });

    onUnmounted(() => {
        document.removeEventListener('fullscreenchange', updateState);
    });

    return {
        isFullscreen,
        toggleFullscreen
    };
}
