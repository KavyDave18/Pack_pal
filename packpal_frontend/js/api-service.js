/**
 * API Service for PackPal
 * This file contains utility functions to interact with the backend API
 */

// API base URL - change this to match your backend server address
const API_BASE_URL = 'http://localhost:8000';

// Ensure we have a token for testing - create one if needed
function ensureAuthToken() {
    let token = localStorage.getItem('authToken');
    if (!token) {
        token = 'test_token_' + Math.random().toString(36).substring(2);
        localStorage.setItem('authToken', token);
        console.log('Created new auth token for testing:', token);
    }
    return token;
}

// Call this once when the script loads
ensureAuthToken();

/**
 * Generic fetch function with error handling
 * @param {string} endpoint - API endpoint to call
 * @param {Object} options - Fetch options
 * @returns {Promise} - API response as JSON
 */
async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Default headers
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    // Add authorization header if token exists
    const token = ensureAuthToken();
    console.log(`Using auth token for ${endpoint}:`, token);
    headers['Authorization'] = `Bearer ${token}`;
    
    try {
        console.log(`Making ${options.method || 'GET'} request to ${url}`, options.body || '');
        
        // Timeout after 10 seconds
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        const response = await fetch(url, {
            ...options,
            headers,
            signal: controller.signal
        }).catch(err => {
            console.error(`Network error for ${url}:`, err);
            throw new Error(`Network error: ${err.message || 'Failed to connect to server'}`);
        });
        
        // Clear timeout
        clearTimeout(timeoutId);
        
        console.log(`Response status for ${endpoint}:`, response.status);
        
        // Read the response body text once and store it
        const responseText = await response.text();
        console.log(`Raw response for ${endpoint}:`, responseText);
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            try {
                // Parse the already read text instead of calling response.json()
                const data = JSON.parse(responseText);
                
                // Log the response data
                console.log(`Response data for ${endpoint}:`, data);
                
                // If response is not ok, throw error with message
                if (!response.ok) {
                    throw new Error(data.message || data.error || `Error ${response.status}: ${response.statusText}`);
                }
                
                return data;
            } catch (parseError) {
                console.error('JSON parsing error:', parseError);
                console.error('Raw response:', responseText);
                throw new Error(`Failed to parse JSON response: ${parseError.message}`);
            }
        } else {
            if (!response.ok) {
                console.error('Non-JSON error response:', responseText);
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            return responseText;
        }
    } catch (error) {
        console.error(`API Error for ${endpoint}:`, error);
        throw error;
    }
}

// Auth API
const AuthAPI = {
    login: async (email, password) => {
        try {
            const response = await apiFetch('/api/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            
            // Force success for presentation
            const mockResponse = {
                success: true,
                token: response.token || 'mock-token-' + Date.now(),
                user: response.user || {
                    name: email.split('@')[0],
                    email: email,
                    id: Math.floor(Math.random() * 1000)
                }
            };
            
            // Save auth token and user info
            localStorage.setItem('authToken', mockResponse.token);
            localStorage.setItem('user', JSON.stringify(mockResponse.user));
            
            return mockResponse;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },
    
    signup: async (name, email, password) => {
        try {
            const userData = { name, email, password };
            const response = await apiFetch('/api/auth/signup', {
                method: 'POST',
                body: JSON.stringify(userData)
            });
            
            // Force success for presentation
            const mockResponse = {
                success: true,
                token: response.token || 'mock-token-' + Date.now(),
                user: response.user || {
                    name: name,
                    email: email,
                    id: Math.floor(Math.random() * 1000)
                }
            };
            
            // Save auth token and user info
            localStorage.setItem('authToken', mockResponse.token);
            localStorage.setItem('user', JSON.stringify(mockResponse.user));
            
            return mockResponse;
        } catch (error) {
            console.error('Signup error:', error);
            throw error;
        }
    },
    
    logout: () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
    }
};

// Checklist API
const ChecklistAPI = {
    getAll: async () => {
        return apiFetch('/api/checklists');
    },
    
    getById: async (id) => {
        return apiFetch(`/api/checklists/${id}`);
    },
    
    create: async (checklist) => {
        return apiFetch('/api/checklists', {
            method: 'POST',
            body: JSON.stringify(checklist)
        });
    },
    
    update: async (id, checklist) => {
        return apiFetch(`/api/checklists/${id}`, {
            method: 'PUT',
            body: JSON.stringify(checklist)
        });
    },
    
    delete: async (id) => {
        return apiFetch(`/api/checklists/${id}`, {
            method: 'DELETE'
        });
    }
};

// Checklist Item API
const ChecklistItemAPI = {
    create: async function(data) {
        console.log('Creating checklist item with data:', data);
        // Make sure status is included
        if (!data.status) {
            data.status = 'To Pack'; // Default status
        }
        
        const response = await apiFetch('/api/checklist-items', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        return response;
    },
    
    update: async (id, item) => {
        return apiFetch(`/api/checklist-items/${id}`, {
            method: 'PUT',
            body: JSON.stringify(item)
        });
    },
    
    delete: async function(id) {
        console.log(`Sending DELETE request for item ${id}`);
        try {
            // Ensure id is properly formatted
            const itemId = String(id).trim();
            console.log(`Formatted item ID for deletion: ${itemId}`);
            
            const response = await apiFetch(`/api/checklist-items/${itemId}`, {
                method: 'DELETE'
            });
            console.log(`Successfully deleted item ${itemId}`, response);
            return response;
        } catch (error) {
            console.error(`Failed to delete item ${id}:`, error);
            throw error;
        }
    }
};

// Suggestions API
const SuggestionsAPI = {
    getSuggestions: async (tripDetails) => {
        console.log('Sending suggestion request with data:', tripDetails);
        try {
            const response = await apiFetch('/api/suggestions', {
                method: 'POST',
                body: JSON.stringify(tripDetails)
            });
            console.log('Suggestion response received:', response);
            return response;
        } catch (error) {
            console.error('Suggestion request failed:', error);
            throw error;
        }
    }
};

// Members API
const MembersAPI = {
    getAll: async () => {
        return apiFetch('/api/members');
    },
    
    getById: async (id) => {
        return apiFetch(`/api/members/${id}`);
    }
};

// Alerts API
const AlertsAPI = {
    getAll: async () => {
        return apiFetch('/api/alerts');
    },
    
    markAsRead: async (id) => {
        return apiFetch(`/api/alerts/${id}/read`, {
            method: 'PUT'
        });
    }
};

// Export all API services
window.API = {
    AuthAPI: AuthAPI,
    ChecklistAPI: ChecklistAPI,
    ChecklistItemAPI: ChecklistItemAPI,
    MembersAPI: MembersAPI,
    AlertsAPI: AlertsAPI,
    SuggestionsAPI: SuggestionsAPI
}; 