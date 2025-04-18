import { fetchWithRetry } from '../apiUtils';
import { NetworkError, TimeoutError } from '../errors';

// Mock global fetch
global.fetch = jest.fn();

describe('fetchWithRetry', () => {
    beforeEach(() => {
        jest.useFakeTimers();
        jest.spyOn(global, 'setTimeout');
        fetch.mockClear();
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    it('succeeds on first attempt', async () => {
        const mockResponse = { ok: true, json: () => Promise.resolve({ data: 'test' }) };
        fetch.mockResolvedValueOnce(mockResponse);

        const response = await fetchWithRetry('/test');
        expect(response).toBe(mockResponse);
        expect(fetch).toHaveBeenCalledTimes(1);
    });

    it('retries on network failure', async () => {
        fetch
            .mockRejectedValueOnce(new NetworkError('Failed'))
            .mockResolvedValueOnce({ ok: true });

        await fetchWithRetry('/test', {}, 2, 100);
        expect(fetch).toHaveBeenCalledTimes(2);
    });

    it('throws TimeoutError on timeout', async () => {
        fetch.mockImplementationOnce(() => new Promise(() => {}));

        const fetchPromise = fetchWithRetry('/test');
        jest.advanceTimersByTime(10000);

        await expect(fetchPromise).rejects.toThrow(TimeoutError);
    });

    it('respects retry limit', async () => {
        fetch.mockRejectedValue(new NetworkError('Failed'));

        await expect(fetchWithRetry('/test', {}, 3, 100))
            .rejects
            .toThrow(NetworkError);

        expect(fetch).toHaveBeenCalledTimes(4); // Initial + 3 retries
    });

    it('implements exponential backoff', async () => {
        fetch.mockRejectedValue(new NetworkError('Failed'));

        try {
            await fetchWithRetry('/test', {}, 2, 1000);
        } catch (error) {
            // Expected to fail
        }

        expect(setTimeout).toHaveBeenCalledTimes(3); // 2 retries + timeout
        expect(setTimeout).toHaveBeenNthCalledWith(1, expect.any(Function), 10000); // Timeout
        expect(setTimeout).toHaveBeenNthCalledWith(2, expect.any(Function), 1000); // First retry
        expect(setTimeout).toHaveBeenNthCalledWith(3, expect.any(Function), 2000); // Second retry
    });
});