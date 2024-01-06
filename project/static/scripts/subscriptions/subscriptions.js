
function follow(author_id) {
    let subscriptionContainer = document.getElementsByClassName('subscription')[0];

    fetch(`/api/follow/${author_id}`, {
        method: 'POST'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    let followButton = document.getElementById('followButton');
    subscriptionContainer.removeChild(followButton);

    let unfollowButton = document.createElement('button');
    unfollowButton.className = 'btn btn-outline-danger';
    unfollowButton.id = 'unfollowButton';
    unfollowButton.innerHTML = 'Відписатись';
    unfollowButton.addEventListener('click', e => unfollow(author_id));
    subscriptionContainer.appendChild(unfollowButton);

    let followersSpan = document.getElementById('followers');
    followersSpan.innerHTML = Number(followersSpan.innerHTML) + 1;

}

function unfollow(author_id) {
    let subscriptionContainer = document.getElementsByClassName('subscription')[0];

    fetch(`/api/unfollow/${author_id}`, {
        method: 'POST'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    let unfollowButton = document.getElementById('unfollowButton');
    subscriptionContainer.removeChild(unfollowButton);

    let followButton = document.createElement('button');
    followButton.className = 'btn btn-outline-success';
    followButton.id = 'followButton';
    followButton.innerHTML = 'Підписатись';
    followButton.addEventListener('click', e => follow(author_id));
    subscriptionContainer.appendChild(followButton);

    let followersSpan = document.getElementById('followers');
    followersSpan.innerHTML = Number(followersSpan.innerHTML) - 1;

}
