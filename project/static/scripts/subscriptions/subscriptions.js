
function follow(user_id, category, status=true) {
    status = Boolean(status);
    
    let subscriptionContainer = document.getElementsByClassName(`subscription-${category}`)[0];

    fetch(`/api/follow/${category}/${user_id}`, {
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
        if (status) {
            unfollowText = 'Відписатись';
        } else {
            unfollowText = 'Скасувати запит на підписку';
        }
    } else if (category === 'topic') {
        unfollowText = 'Не стежити';
    } else {
        return 0;
    }

    if (!status && category === 'user') {
        let unfollowRequestButton = document.createElement('button');
        unfollowRequestButton.className = 'btn btn-outline-warning';
        unfollowRequestButton.id = 'unfollowRequestButton';
        unfollowRequestButton.innerHTML = unfollowText;
        unfollowRequestButton.addEventListener('click', e => unfollowRequest(user_id, category, status));
        subscriptionContainer.appendChild(unfollowRequestButton);

    } else {
        let unfollowButton = document.createElement('button');
        unfollowButton.className = 'btn btn-outline-danger';
        unfollowButton.id = 'unfollowButton';
        unfollowButton.innerHTML = unfollowText;
        unfollowButton.addEventListener('click', e => unfollow(user_id, category, status));
        subscriptionContainer.appendChild(unfollowButton);

    }

    let followersSpan = document.getElementById('followers');
    followersSpan.innerHTML = Number(followersSpan.innerHTML) + 1;

}

function unfollow(user_id, category, status=true) {
    status = Boolean(status);

    let subscriptionContainer = document.getElementsByClassName(`subscription-${category}`)[0];

    fetch(`/api/unfollow/${category}/${user_id}`, {
        method: 'DELETE'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    let unfollowButton = document.getElementById('unfollowButton');
    subscriptionContainer.removeChild(unfollowButton);

    let followText;
    if (category === 'user') {
        if (status) {
            followText = 'Підписатись';
        } else {
            followText = 'Надіслати запит на підписку';
        }
    } else if (category === 'topic') {
        followText = 'Стежити';
    } else {
        return 0;
    }

    if (!status && category === 'user') {
        let followRequestButton = document.createElement('button');
        followRequestButton.className = 'btn btn-outline-warning';
        followRequestButton.id = 'followRequestButton';
        followRequestButton.innerHTML = followText;
        followRequestButton.addEventListener('click', e => followRequest(user_id, category, status));
        subscriptionContainer.appendChild(followRequestButton);

    } else {
        let followButton = document.createElement('button');
        followButton.className = 'btn btn-outline-success';
        followButton.id = 'followButton';
        followButton.innerHTML = followText;
        followButton.addEventListener('click', e => follow(user_id, category, status));
        subscriptionContainer.appendChild(followButton);

    }

    let followersSpan = document.getElementById('followers');
    followersSpan.innerHTML = Number(followersSpan.innerHTML) - 1;

}

function followRequest(user_id, category, status=true) {
    status = Boolean(status);
    
    let subscriptionContainer = document.getElementsByClassName(`subscription-${category}`)[0];

    fetch(`/api/follow/request/${category}/${user_id}`, {
        method: 'POST'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    let followRequestButton = document.getElementById('followRequestButton');
    subscriptionContainer.removeChild(followRequestButton);

    let unfollowText;
    if (category === 'user') {
        if (status) {
            unfollowText = 'Відписатись';
        } else {
            unfollowText = 'Скасувати запит на підписку';
        }
    } else {
        return 0;
    }

    let unfollowRequestButton = document.createElement('button');
    unfollowRequestButton.className = 'btn btn-outline-warning';
    unfollowRequestButton.id = 'unfollowRequestButton';
    unfollowRequestButton.innerHTML = unfollowText;
    unfollowRequestButton.addEventListener('click', e => unfollowRequest(user_id, category, status));
    subscriptionContainer.appendChild(unfollowRequestButton);

}

function unfollowRequest(user_id, category, status=true) {
    status = Boolean(status);
    
    let subscriptionContainer = document.getElementsByClassName(`subscription-${category}`)[0];

    fetch(`/api/unfollow/request/${category}/${user_id}`, {
        method: 'DELETE'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    let unfollowRequestButton = document.getElementById('unfollowRequestButton');
    subscriptionContainer.removeChild(unfollowRequestButton);

    let followText;
    if (category === 'user') {
        if (status) {
            followText = 'Підписатись';
        } else {
            followText = 'Надіслати запит на підписку';
        }
    } else {
        return 0;
    }

    let followRequestButton = document.createElement('button');
    followRequestButton.className = 'btn btn-outline-warning';
    followRequestButton.id = 'followRequestButton';
    followRequestButton.innerHTML = followText;
    followRequestButton.addEventListener('click', e => followRequest(user_id, category, status));
    subscriptionContainer.appendChild(followRequestButton);

}

function acceptFollowRequest(author_id, user_id) {
    let followRequestContainer = document.getElementById(`follow_request_${user_id}`);

    fetch(`/api/follow/request/user/${author_id}/accept/${user_id}`, {
        method: 'POST'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    followRequestContainer.remove();

    let followRequestsSpan = document.getElementById('followRequests');
    followRequestsSpan.innerHTML = Number(followRequestsSpan.innerHTML) - 1;

    let followersSpan = document.getElementById('followers');
    followersSpan.innerHTML = Number(followersSpan.innerHTML) + 1;

}

function rejectFollowRequest(author_id, user_id) {
    let followRequestContainer = document.getElementById(`follow_request_${user_id}`);

    fetch(`/api/follow/request/user/${author_id}/reject/${user_id}`, {
        method: 'DELETE'
    })
    .catch(error => {
        console.error(error);
        return 0;
    });

    followRequestContainer.remove();

    let followRequestsSpan = document.getElementById('followRequests');
    followRequestsSpan.innerHTML = Number(followRequestsSpan.innerHTML) - 1;

}

function deleteFollower(author_id, user_id) {
    let followerContainer = document.getElementById(`follower_${user_id}`);

    fetch(`/api/follow/user/${author_id}/delete/${user_id}`, {
        method: 'DELETE'
    })
    .catch(error => {
        console.error(error);
    });

    followerContainer.remove();

    let followersSpan = document.getElementById('followers');
    followersSpan.innerHTML = Number(followersSpan.innerHTML) - 1;

}
