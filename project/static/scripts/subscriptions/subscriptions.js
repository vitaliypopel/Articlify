
function follow(id, category) {
    let subscriptionContainer = document.getElementsByClassName(`subscription-${category}`)[0];

    fetch(`/api/follow/${category}/${id}`, {
        method: 'POST'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    let followButton = document.getElementById('followButton');
    subscriptionContainer.removeChild(followButton);

    let unfollowText;
    if (category === 'user') {
        unfollowText = 'Відписатись';
    } else if (category === 'topic') {
        unfollowText = 'Не стежити';
    } else {
        return 0;
    }

    let unfollowButton = document.createElement('button');
    unfollowButton.className = 'btn btn-outline-danger';
    unfollowButton.id = 'unfollowButton';
    unfollowButton.innerHTML = unfollowText;
    unfollowButton.addEventListener('click', e => unfollow(id, category));
    subscriptionContainer.appendChild(unfollowButton);

    let followersSpan = document.getElementById('followers');
    followersSpan.innerHTML = Number(followersSpan.innerHTML) + 1;

}

function unfollow(id, category) {
    let subscriptionContainer = document.getElementsByClassName(`subscription-${category}`)[0];

    fetch(`/api/unfollow/${category}/${id}`, {
        method: 'POST'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    let unfollowButton = document.getElementById('unfollowButton');
    subscriptionContainer.removeChild(unfollowButton);

    let followText;
    if (category === 'user') {
        followText = 'Підписатись';
    } else if (category === 'topic') {
        followText = 'Стежити';
    } else {
        return 0;
    }

    let followButton = document.createElement('button');
    followButton.className = 'btn btn-outline-success';
    followButton.id = 'followButton';
    followButton.innerHTML = followText;
    followButton.addEventListener('click', e => follow(id, category));
    subscriptionContainer.appendChild(followButton);

    let followersSpan = document.getElementById('followers');
    followersSpan.innerHTML = Number(followersSpan.innerHTML) - 1;

}
