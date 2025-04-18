/**
 * Structured logging utility for frontend
 */

const LOG_LEVELS = {
    INFO: 'info',
    WARN: 'warn',
    ERROR: 'error',
    DEBUG: 'debug'
};

/**
 * Creates a structured log entry
 * @param {string} event - The event name
 * @param {Object} data - Additional data to log
 * @param {string} level - Log level (info, warn, error, debug)
 */
export function log(event, data = {}, level = LOG_LEVELS.INFO) {
    const logEntry = {
        event,
        ...data,
        timestamp: new Date().toISOString(),
        level
    };

    switch (level) {
        case LOG_LEVELS.ERROR:
            console.error(JSON.stringify(logEntry));
            break;
        case LOG_LEVELS.WARN:
            console.warn(JSON.stringify(logEntry));
            break;
        case LOG_LEVELS.DEBUG:
            console.debug(JSON.stringify(logEntry));
            break;
        default:
            console.log(JSON.stringify(logEntry));
    }
}

/**
 * Log API call events
 * @param {string} url - The API endpoint URL
 * @param {string} method - HTTP method
 * @param {string} status - Response status
 * @param {Object} additionalData - Any additional data to log
 */
export function logApiCall(url, method, status, additionalData = {}) {
    log('API_CALL', {
        url,
        method,
        status,
        ...additionalData
    });
}

/**
 * Log error events
 * @param {Error} error - The error object
 * @param {Object} context - Additional context about the error
 */
export function logError(error, context = {}) {
    log('ERROR', {
        error: {
            name: error.name,
            message: error.message,
            stack: error.stack
        },
        ...context
    }, LOG_LEVELS.ERROR);
}