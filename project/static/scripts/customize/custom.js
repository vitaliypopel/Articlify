
function getSystemTheme() {
    let darkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (darkTheme) {
        return 'dark';
    } else {
        return 'light';
    }
}


function setTheme(theme) {
    if (theme === 'auto') {
        theme = getSystemTheme();
    }

    htmlElement = document.documentElement;
    htmlElement.setAttribute('data-bs-theme', theme);

    setCookieTheme(theme)
}


function setCookieTheme(theme) {
    fetch('/api/change-theme', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            theme: theme
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Щось пішло не так! Спробуйте ще раз.');
        }
    })
    .catch(error => {
        alert('Error:', error);
    })
}
