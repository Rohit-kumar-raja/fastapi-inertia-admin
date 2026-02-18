/**
 * Deletes a cookie by name.
 * Uses legacy document.cookie manipulation as a fallback or direct method where Cookie Store API is unavailable.
 * @param name - The name of the cookie to delete
 * @param path - The path of the cookie (default: '/')
 */
export function deleteCookie(name: string, path: string = '/') {
    // eslint-disable-next-line unicorn/no-document-cookie
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${path};`;
}
