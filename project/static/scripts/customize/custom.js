
function getSystemTheme() {
    let darkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (darkTheme) {
        return 'dark';
    } else {
        return 'light';
    }
}

let systemTheme = getSystemTheme();
console.log(systemTheme);
