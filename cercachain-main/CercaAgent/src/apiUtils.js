import { NetworkError, TimeoutError } from './errors.js';

/**
 * Fetches data with retry mechanism and timeout handling
 * @param {string} url - The URL to fetch from
 * @param {Object} options - Fetch options
 * @param {number} retries - Number of retry attempts
 * @param {number} backoff - Initial backoff time in milliseconds
 * @returns {Promise<Response>} The fetch response
 */
export async function fetchWithRetry(url, options = {}, retries = 3, backoff = 1000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new NetworkError(`HTTP error! status: ${response.status}`);
        }
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        
        if (error.name === 'AbortError') {
            throw new TimeoutError('Request timed out');
        }

        if ((error instanceof NetworkError || error.name === 'TypeError') && retries > 0) {
            await new Promise(resolve => setTimeout(resolve, backoff));
            return fetchWithRetry(url, options, retries - 1, backoff * 2);
        }
        throw error;
    }
}