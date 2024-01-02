
function changeUsername() {
    let closeButton = document.getElementById('cancelChangeUsernameButton');
    closeButton.click();

    let newUsername = document.getElementById('username').value;

    req = {'new_username': newUsername};
    
    fetch('/api/change-username',{
        method: "PATCH",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(req)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.error(error);
    })

}

function changeEmail() {
    let closeButton = document.getElementById('cancelChangeEmailButton');
    closeButton.click();

    let newEmail = document.getElementById('email').value;

    req = {'new_email': newEmail};
    
    fetch('/api/change-email',{
        method: "PATCH",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(req)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.error(error);
    })

}

function changeProfilePicture() {
    let closeButton = document.getElementById('cancelChangeProfilePictureButton');

    let newProfilePicture = document.getElementById('profilePicture');
    let profilePictureFile = newProfilePicture.files[0];

    let types = ['image/png', 'image/jpg', 'image/jpeg'];

    if (!types.includes(profilePictureFile.type)) {
        alert('Фото профілю повинне бути розширення .png або .jpg');
        return 0;
    }

    if (profilePictureFile.size > 300 * 1024) {
        alert('Розмір файлу повинен бути не більше ніж 300 кілобайт');
        return 0;
    }

    closeButton.click();
    

}
