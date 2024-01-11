
function changeUsername() {
    let closeButton = document.getElementById('cancelChangeUsernameButton');
    closeButton.click();

    let newUsername = document.getElementById('username').value;

    req = {'new_username': newUsername};
    
    fetch('/api/change/username', {
        method: 'PATCH',
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
    });

}

function changeEmail() {
    let closeButton = document.getElementById('cancelChangeEmailButton');
    closeButton.click();

    let newEmail = document.getElementById('email').value;

    req = {'new_email': newEmail};
    
    fetch('/api/change/email', {
        method: 'PATCH',
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
    });

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

    let formData = new FormData();
    formData.append('new_profile_picture', profilePictureFile);


    fetch('/api/change/profile-picture', {
        method: 'PATCH',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.error(error);
    });

}

function deleteProfilePicture() {
    let closeButton = document.getElementById('cancelChangeProfilePictureButton');
    closeButton.click();

    fetch('/api/delete/profile-picture', {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.error(error);
    });
    
}

function changeBio() {
    let closeButton = document.getElementById('cancelChangeBioButton');
    closeButton.click();

    let newBio = document.getElementById('bio').value;
    
    req = {'new_bio': newBio};

    fetch('/api/change/bio', {
        method: 'PATCH',
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
    });

}

function changeProfileStatus() {
    let closeButton = document.getElementById('cancelChangeProfileStatusButton');
    closeButton.click();

    let newProfileStatus = document.getElementById('profileStatus').value;

    req = {};

    if (newProfileStatus === 'public') {
        req.new_profile_status = true;
    } else if (newProfileStatus === 'private') {
        req.new_profile_status = false;
    } else {
        alert('Щось пішло не так! Спробуйте ще раз');
        return 0;
    }

    fetch('/api/change/profile-status', {
        method: 'PATCH',
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
    });

}
