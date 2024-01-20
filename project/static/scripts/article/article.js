
function putLike(articleID) {

    fetch(`/api/articles/${articleID}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.bad) {
            alert(data.bad);
            return 0;
        }
    })
    .catch(error => {
        console.log(error);
        return 0;
    });

    let likesElements = document.getElementsByClassName('likes');
    for (let likesElement of likesElements) {
        likesElement.innerHTML = Number(likesElement.innerHTML) + 1;
    }

    let likeButtons = document.getElementsByClassName('like-article');
    for (var i = 0; i < 2; i++) {
        likeButtons[0].remove();
    }

    let likeButtonContainer = document.getElementsByClassName('like-article-container');
    for (let container of likeButtonContainer) {
        let likeButton = document.createElement('button');
        likeButton.type = 'button';
        likeButton.className = 'like-article btn p-1';
        likeButton.addEventListener('click', foo => removeLike(articleID));
        
        let icon = document.createElement('i');
        icon.className = 'fa-solid fa-heart';
        likeButton.appendChild(icon);

        container.insertBefore(likeButton, container.firstChild);
    }
}

function removeLike(articleID) {

    fetch(`/api/articles/${articleID}/like`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.bad) {
            alert(data.bad);
            return 0;
        }
    })
    .catch(error => {
        console.log(error);
        return 0;
    });

    let likesElements = document.getElementsByClassName('likes');
    for (let likesElement of likesElements) {
        likesElement.innerHTML = Number(likesElement.innerHTML) - 1;
    }

    let likeButtons = document.getElementsByClassName('like-article');
    for (var i = 0; i < 2; i++) {
        likeButtons[0].remove();
    }

    let likeButtonContainer = document.getElementsByClassName('like-article-container');
    for (let container of likeButtonContainer) {
        let likeButton = document.createElement('button');
        likeButton.type = 'button';
        likeButton.className = 'like-article btn p-1';
        likeButton.addEventListener('click', foo => putLike(articleID));
        
        let icon = document.createElement('i');
        icon.className = 'fa-regular fa-heart';
        likeButton.appendChild(icon);

        container.insertBefore(likeButton, container.firstChild);
    }
}
