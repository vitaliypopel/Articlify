
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

    fetch(`/api/articles/${articleLink}/comment/post`, {
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
        console.error(error);
        return 0;
    });
}

function deleteComment(articleLink, commentID) {
    let request = {
        'comment_id': commentID
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
        console.log(data);
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.log(error);
        return 0;
    });
}

function addSavedArticle(articleLink) {
    fetch(`/api/articles/${articleLink}/saved/add`, {
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

    let savedArticleButtons = document.getElementsByClassName('saved-article');
    for (var i = 0; i < 2; i++) {
        savedArticleButtons[0].remove();
    }

    let savedArticleContainer = document.getElementsByClassName('saved-article-container');
    for (let container of savedArticleContainer) {
        let savedArticleButton = document.createElement('button');
        savedArticleButton.type = 'button';
        savedArticleButton.className = 'saved-article btn p-1';
        savedArticleButton.addEventListener('click', foo => deleteSavedArticle(articleLink));
        
        let icon = document.createElement('i');
        icon.className = 'fa-solid fa-bookmark';
        savedArticleButton.appendChild(icon);

        container.appendChild(savedArticleButton);
    }
}

function deleteSavedArticle(articleLink) {
    fetch(`/api/articles/${articleLink}/saved/delete`, {
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

    let savedArticleButtons = document.getElementsByClassName('saved-article');
    for (var i = 0; i < 2; i++) {
        savedArticleButtons[0].remove();
    }

    let savedArticleContainer = document.getElementsByClassName('saved-article-container');
    for (let container of savedArticleContainer) {
        let savedArticleButton = document.createElement('button');
        savedArticleButton.type = 'button';
        savedArticleButton.className = 'saved-article btn p-1';
        savedArticleButton.addEventListener('click', foo => addSavedArticle(articleLink));
        
        let icon = document.createElement('i');
        icon.className = 'fa-regular fa-bookmark';
        savedArticleButton.appendChild(icon);

        container.appendChild(savedArticleButton);
    }
}

function copyLink(link) {
    let clipboard = navigator.clipboard;

    clipboard.writeText(link)
    .then(function() {
        alert('Посилання скопійоване!');
    })
    .catch(error => {
        console.error(error);
    });
}
