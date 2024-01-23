
function putLike(articleLink) {

    fetch(`/api/articles/${articleLink}/like/put`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
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
        likeButton.addEventListener('click', foo => removeLike(articleLink));
        
        let icon = document.createElement('i');
        icon.className = 'fa-solid fa-heart';
        likeButton.appendChild(icon);

        container.insertBefore(likeButton, container.firstChild);
    }
}

function removeLike(articleLink) {

    fetch(`/api/articles/${articleLink}/like/remove`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
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
        likeButton.addEventListener('click', foo => putLike(articleLink));
        
        let icon = document.createElement('i');
        icon.className = 'fa-regular fa-heart';
        likeButton.appendChild(icon);

        container.insertBefore(likeButton, container.firstChild);
    }
}

function postComment(articleLink) {
    let newComment = document.getElementById('comment').value;
    
    let request = {
        'new_comment': newComment
    };

    fetch(`/api/articles/${articleLink}/comment/write`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.log(error);
        return 0;
    });
}

function patchComment(articleLink, commentID) {
    let newComment = document.getElementById('comment').value;
    
    let request = {
        'comment_id': commentID,
        'new_comment': newComment
    };

    fetch(`/api/articles/${articleLink}/comment/edit`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.log(error);
        return 0;
    });
}

function deleteComment(articleLink, commentID) {
    let newComment = document.getElementById('comment').value;
    
    let request = {
        'comment_id': commentID,
        'new_comment': newComment
    };

    fetch(`/api/articles/${articleLink}/comment/delete`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.log(error);
        return 0;
    });
}
