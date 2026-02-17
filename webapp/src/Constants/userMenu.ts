
import {
    faUser, faCog, faSignOutAlt
} from "@fortawesome/free-solid-svg-icons";
import { useUserStore } from "@/Store/userStore";

const userStore = useUserStore();

export const userMenuItems = ref<Array<Record<string, any>>>([
    {
        label: 'Profile',
        icon: faUser,
        command: () => console.log('Profile')
    },
    {
        label: 'Settings',
        icon: faCog,
        command: () => console.log('Settings')
    },
    {
        separator: true
    },
    {
        label: 'Logout',
        icon: faSignOutAlt,
        command: () => userStore.logout()
    }
])