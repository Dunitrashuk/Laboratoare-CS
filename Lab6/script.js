const firebaseConfig = {
    apiKey: "AIzaSyB8dob1RX7spAmhUtDi8Df_lT0FaFidc_Y",
    authDomain: "cs-lab-6.firebaseapp.com",
    projectId: "cs-lab-6",
    storageBucket: "cs-lab-6.appspot.com",
    messagingSenderId: "171594688198",
    appId: "1:171594688198:web:f3213a058f19e5704799c7",
    measurementId: "G-3S56E315KL"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
var ui = new firebaseui.auth.AuthUI(firebase.auth());


var uiConfig = {
    callbacks: {
        signInSuccessWithAuthResult: function (authResult, redirectUrl) {
            // User successfully signed in.
            // Return type determines whether we continue the redirect automatically
            // or whether we leave that to developer to handle.
            return true;
        },
        uiShown: function () {
            // The widget is rendered.
            // Hide the loader.
            document.getElementById('loader').style.display = 'none';
        }
    },
    // Will use popup for IDP Providers sign-in flow instead of the default, redirect.
    signInFlow: 'popup',
    signInSuccessUrl: 'https://cs-auth-566f7.web.app/success.html',
    signInOptions: [
        // Leave the lines as is for the providers you want to offer your users.
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.FacebookAuthProvider.PROVIDER_ID,
    ],
    // Terms of service url.
    tosUrl: '<your-tos-url>',
    // Privacy policy url.
    privacyPolicyUrl: '<your-privacy-policy-url>'
};
ui.start('#firebaseui-auth-container', uiConfig);