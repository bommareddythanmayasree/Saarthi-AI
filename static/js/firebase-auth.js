// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { 
    getAuth, 
    signInWithEmailAndPassword, 
    createUserWithEmailAndPassword, 
    signOut, 
    onAuthStateChanged,
    GoogleAuthProvider,
    signInWithPopup
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyD7g3F2x-LsPxU-kgS3uipSJ9HH3LhwKrQ",
    authDomain: "saarthi-ai-76a85.firebaseapp.com",
    projectId: "saarthi-ai-76a85",
    storageBucket: "saarthi-ai-76a85.firebasestorage.app",
    messagingSenderId: "476646027712",
    appId: "1:476646027712:web:7ee59d22de004910a7d825"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Initialize Google Auth Provider
const googleProvider = new GoogleAuthProvider();
// Add additional scopes if needed
googleProvider.addScope('profile');
googleProvider.addScope('email');
// Set custom parameters
googleProvider.setCustomParameters({
    prompt: 'select_account'
});

// Export auth instance for use in other modules
export { auth };

// Login function
export async function login(email, password) {
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        return { success: true, user: userCredential.user };
    } catch (error) {
        return { success: false, error: getReadableErrorMessage(error.code) };
    }
}

// Signup function
export async function signup(email, password) {
    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        return { success: true, user: userCredential.user };
    } catch (error) {
        return { success: false, error: getReadableErrorMessage(error.code) };
    }
}

// Logout function
export async function logout() {
    try {
        await signOut(auth);
        return { success: true };
    } catch (error) {
        return { success: false, error: getReadableErrorMessage(error.code) };
    }
}

// Google Sign-In function
export async function signInWithGoogle() {
    try {
        // Log attempt for debugging
        console.log('Attempting Google Sign-In...');
        
        const result = await signInWithPopup(auth, googleProvider);
        console.log('Google Sign-In successful:', result.user.email);
        
        return { success: true, user: result.user };
    } catch (error) {
        // Log detailed error for debugging
        console.error('Google Sign-In Error:', error.code, error.message);
        console.error('Full error object:', error);
        
        // Handle specific popup errors
        if (error.code === 'auth/popup-closed-by-user') {
            return { success: false, error: 'Sign-in popup was closed. Please try again.' };
        }
        if (error.code === 'auth/cancelled-popup-request') {
            return { success: false, error: 'Sign-in was cancelled.' };
        }
        if (error.code === 'auth/unauthorized-domain') {
            return { success: false, error: 'This domain is not authorized. Please contact the administrator to add this domain to Firebase Console.' };
        }
        
        return { success: false, error: getReadableErrorMessage(error.code) };
    }
}

// Check authentication state
export function checkAuthState(callback) {
    return onAuthStateChanged(auth, callback);
}

// Get current user
export function getCurrentUser() {
    return auth.currentUser;
}

// Convert Firebase error codes to readable messages
function getReadableErrorMessage(errorCode) {
    const errorMessages = {
        'auth/invalid-email': 'Invalid email address format.',
        'auth/user-disabled': 'This account has been disabled.',
        'auth/user-not-found': 'No account found with this email.',
        'auth/wrong-password': 'Incorrect password.',
        'auth/email-already-in-use': 'An account with this email already exists.',
        'auth/weak-password': 'Password should be at least 6 characters.',
        'auth/operation-not-allowed': 'Email/password accounts are not enabled.',
        'auth/too-many-requests': 'Too many failed attempts. Please try again later.',
        'auth/network-request-failed': 'Network error. Please check your connection.',
        'auth/invalid-credential': 'Invalid email or password.',
        'auth/popup-blocked': 'Sign-in popup was blocked. Please allow popups for this site.',
        'auth/popup-closed-by-user': 'Sign-in popup was closed. Please try again.',
        'auth/cancelled-popup-request': 'Sign-in was cancelled.',
        'auth/account-exists-with-different-credential': 'An account already exists with the same email but different sign-in credentials.',
        'auth/unauthorized-domain': 'This domain is not authorized for OAuth operations. Please add it to the Firebase Console authorized domains list.',
        'auth/operation-not-supported-in-this-environment': 'This operation is not supported in this environment. Make sure you are using HTTPS.',
        'auth/timeout': 'The operation has timed out. Please try again.',
        'auth/missing-android-pkg-name': 'An Android Package Name must be provided.',
        'auth/missing-continue-uri': 'A continue URL must be provided.',
        'auth/missing-ios-bundle-id': 'An iOS Bundle ID must be provided.',
        'auth/invalid-continue-uri': 'The continue URL provided is invalid.',
        'auth/unauthorized-continue-uri': 'The domain of the continue URL is not whitelisted.'
    };
    
    return errorMessages[errorCode] || `An error occurred: ${errorCode}. Please try again.`;
}

// Protect page - redirect to login if not authenticated
export function protectPage(redirectUrl = '/login') {
    return new Promise((resolve, reject) => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            unsubscribe();
            if (user) {
                resolve(user);
            } else {
                window.location.href = redirectUrl;
                reject(new Error('Not authenticated'));
            }
        });
    });
}
