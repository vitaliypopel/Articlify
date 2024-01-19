$(document).ready(
    function () {
        $(".sortable-list").sortable({
            handle: ".drag-handle",
            axis: "y",
        });
    }
);

function deleteElement(elementInputGroup) {
    if (!elementInputGroup) {
        alert('Щось пішло не так! Спробуйте ще раз');
        return 0;
    }

    let container = elementInputGroup.parentElement;
    container.remove();
}

function addElement() {
    let elementType = document.getElementById('elementType').value;

    if (!elementType) {
        alert('Щось пішло не так! Спробуйте ще раз');
        return 0;
    }

    let container = document.getElementsByClassName('article')[0];
    let newElement;

    switch (elementType) {
        case 'subtitle':
            newElement = addSubtitle();
            break;
        case 'text':
            newElement = addText();
            break;
        case 'hyperlink':
            newElement = addHyperlink();
            break;
        case 'textarea':
            newElement = addTextarea();
            break;
        case 'photo':
            newElement = addPhoto();
            break;
        case 'code':
            newElement = addCode();
            break;
        case 'pass':
            newElement = addPass();
            break;
        default:
            alert('Щось пішло не так! Спробуйте ще раз');
            return 0;
    }

    container.appendChild(newElement);
}

function addSubtitle() {
    let container = document.createElement('div');
    container.className = 'subtitle scrolable-item mt-3 mb-3';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group w-100 d-flex flex-nowrap';

    let elementGrab = document.createElement('span');
    elementGrab.className = 'input-group-text bg-transparent drag-handle border-end-0';

    let elementGrabIcon = document.createElement('i');
    elementGrabIcon.className = 'fa-solid fa-bars';

    elementGrab.appendChild(elementGrabIcon);

    let elementSpan = document.createElement('span');
    elementSpan.className = 'input-group-text bg-transparent w-25';
    elementSpan.innerHTML = 'Підзаголовок';

    let elementInput = document.createElement('input');
    elementInput.className = 'content form-control';
    elementInput.type = 'text';
    elementInput.placeholder = 'Підзаголовок';
    elementInput.minLength = '1';
    elementInput.maxLength = '100';

    let elementDeleteButton = document.createElement('button');
    elementDeleteButton.className = 'btn btn-outline-danger border';
    elementDeleteButton.type = 'button';
    elementDeleteButton.addEventListener('click', foo => deleteElement(elementInputGroup));
    
    let elementButtonIcon = document.createElement('i');
    elementButtonIcon.className = 'fa-solid fa-xmark';

    elementDeleteButton.appendChild(elementButtonIcon);

    elementInputGroup.appendChild(elementGrab);
    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementInput);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addText() {
    let container = document.createElement('div');
    container.className = 'text sortable-item mt-3 mb-3';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group w-100 d-flex flex-nowrap';

    let elementGrab = document.createElement('span');
    elementGrab.className = 'input-group-text bg-transparent drag-handle border-end-0';

    let elementGrabIcon = document.createElement('i');
    elementGrabIcon.className = 'fa-solid fa-bars';

    elementGrab.appendChild(elementGrabIcon);

    let elementSpan = document.createElement('span');
    elementSpan.className = 'w-25';

    let elementSelect = document.createElement('select');
    elementSelect.className = 'text-type form-select rounded-0';
    
    let options = [
        {'value': 'normal', 'text': 'Звичайний'},
        {'value': 'bold', 'text': 'Товстий'},
        {'value': 'italic', 'text': 'Курсив'}
    ]

    for (var element of options) {
        var option = document.createElement('option');
        option.value = element.value;
        option.text = element.text;
        elementSelect.appendChild(option);
    }

    elementSpan.appendChild(elementSelect);

    let elementInput = document.createElement('input');
    elementInput.className = 'content form-control';
    elementInput.type = 'text';
    elementInput.placeholder = 'Рядок';
    elementInput.minLength = '1';
    elementInput.maxLength = '100';

    let elementDeleteButton = document.createElement('button');
    elementDeleteButton.className = 'btn btn-outline-danger border';
    elementDeleteButton.type = 'button';
    elementDeleteButton.addEventListener('click', foo => deleteElement(elementInputGroup));
    
    let elementButtonIcon = document.createElement('i');
    elementButtonIcon.className = 'fa-solid fa-xmark';

    elementDeleteButton.appendChild(elementButtonIcon);

    elementInputGroup.appendChild(elementGrab);
    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementInput);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addHyperlink() {
    let container = document.createElement('div');
    container.className = 'hyperlink sortable-item mt-3 mb-3';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group w-100 d-flex flex-nowrap';

    let elementGrab = document.createElement('span');
    elementGrab.className = 'input-group-text bg-transparent drag-handle border-end-0';

    let elementGrabIcon = document.createElement('i');
    elementGrabIcon.className = 'fa-solid fa-bars';

    elementGrab.appendChild(elementGrabIcon);    

    let elementGroup = document.createElement('div');
    elementGroup.className = 'w-auto flex-grow-1';

    let elementLinkGroup = document.createElement('div');
    elementLinkGroup.className = 'input-group w-100';

    let elementLinkSpan = document.createElement('span');
    elementLinkSpan.className = 'input-group-text bg-transparent w-25 rounded-0 border-bottom-0';
    elementLinkSpan.innerHTML = 'Посилання';

    let elementLinkInput = document.createElement('input');
    elementLinkInput.className = 'link form-control rounded-0 border-bottom-0';
    elementLinkInput.type = 'text';
    elementLinkInput.placeholder = 'Посилання';
    elementLinkInput.minLength = '1';
    elementLinkInput.maxLength = '200';

    elementLinkGroup.appendChild(elementLinkSpan);
    elementLinkGroup.appendChild(elementLinkInput);

    let elementSignGroup = document.createElement('div');
    elementSignGroup.className = 'input-group w-100';

    let elementSignSpan = document.createElement('span');
    elementSignSpan.className = 'input-group-text bg-transparent w-25 rounded-0';
    elementSignSpan.innerHTML = 'Підпис';

    let elementSignInput = document.createElement('input');
    elementSignInput.className = 'content form-control rounded-0';
    elementSignInput.type = 'text';
    elementSignInput.placeholder = 'Підпис';
    elementSignInput.minLength = '1';
    elementSignInput.maxLength = '100';

    elementSignGroup.appendChild(elementSignSpan);
    elementSignGroup.appendChild(elementSignInput);

    elementGroup.appendChild(elementLinkGroup);
    elementGroup.appendChild(elementSignGroup);

    let elementDeleteButton = document.createElement('button');
    elementDeleteButton.className = 'btn btn-outline-danger border border-start-0';
    elementDeleteButton.type = 'button';
    elementDeleteButton.addEventListener('click', foo => deleteElement(elementInputGroup));
    
    let elementButtonIcon = document.createElement('i');
    elementButtonIcon.className = 'fa-solid fa-xmark';

    elementDeleteButton.appendChild(elementButtonIcon);

    elementInputGroup.appendChild(elementGrab);
    elementInputGroup.appendChild(elementGroup);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addTextarea() {
    let container = document.createElement('div');
    container.className = 'textarea sortable-item mt-3 mb-3';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group w-100 d-flex flex-nowrap';

    let elementGrab = document.createElement('span');
    elementGrab.className = 'input-group-text bg-transparent drag-handle border-end-0';

    let elementGrabIcon = document.createElement('i');
    elementGrabIcon.className = 'fa-solid fa-bars';

    elementGrab.appendChild(elementGrabIcon);

    let elementSpan = document.createElement('span');
    elementSpan.className = 'input-group w-25';

    let elementSelect = document.createElement('select');
    elementSelect.className = 'text-type form-select rounded-0';
    
    let options = [
        {'value': 'normal', 'text': 'Звичайний'},
        {'value': 'bold', 'text': 'Товстий'},
        {'value': 'italic', 'text': 'Курсив'}
    ]

    for (var element of options) {
        var option = document.createElement('option');
        option.value = element.value;
        option.text = element.text;
        elementSelect.appendChild(option);
    }

    elementSpan.appendChild(elementSelect);

    let elementTextarea = document.createElement('textarea');
    elementTextarea.className = 'content form-control';
    elementTextarea.placeholder = 'Абзац';
    elementTextarea.minLength = '1';
    elementTextarea.maxLength = '5000';

    let elementDeleteButton = document.createElement('button');
    elementDeleteButton.className = 'btn btn-outline-danger border';
    elementDeleteButton.type = 'button';
    elementDeleteButton.addEventListener('click', foo => deleteElement(elementInputGroup));
    
    let elementButtonIcon = document.createElement('i');
    elementButtonIcon.className = 'fa-solid fa-xmark';

    elementDeleteButton.appendChild(elementButtonIcon);

    elementInputGroup.appendChild(elementGrab);
    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementTextarea);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addPhoto() {
    let container = document.createElement('div');
    container.className = 'photo sortable-item mt-3 mb-3';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group w-100 d-flex flex-nowrap';

    let elementGrab = document.createElement('span');
    elementGrab.className = 'input-group-text bg-transparent drag-handle border-end-0';

    let elementGrabIcon = document.createElement('i');
    elementGrabIcon.className = 'fa-solid fa-bars';

    elementGrab.appendChild(elementGrabIcon);

    let elementGroup = document.createElement('div');
    elementGroup.className = 'w-auto flex-grow-1';

    let elementPhotoGroup = document.createElement('div');
    elementPhotoGroup.className = 'input-group w-100';

    let elementPhotoSpan = document.createElement('span');
    elementPhotoSpan.className = 'input-group-text bg-transparent w-25 rounded-0 border-bottom-0';
    elementPhotoSpan.innerHTML = 'Фото';

    let elementPhotoInput = document.createElement('input');
    elementPhotoInput.className = 'photo-file form-control rounded-0 border-bottom-0';
    elementPhotoInput.type = 'file';

    elementPhotoGroup.appendChild(elementPhotoSpan);
    elementPhotoGroup.appendChild(elementPhotoInput);

    let elementDescriptionGroup = document.createElement('div');
    elementDescriptionGroup.className = 'input-group w-100';

    let elementDescriptionSpan = document.createElement('span');
    elementDescriptionSpan.className = 'input-group-text bg-transparent w-25 rounded-0';
    elementDescriptionSpan.innerHTML = 'Опис';

    let elementDescriptionInput = document.createElement('input');
    elementDescriptionInput.className = 'content form-control rounded-0';
    elementDescriptionInput.type = 'text';
    elementDescriptionInput.placeholder = 'Опис фотографії';
    elementDescriptionInput.minLength = '1';
    elementDescriptionInput.maxLength = '250';

    elementDescriptionGroup.appendChild(elementDescriptionSpan);
    elementDescriptionGroup.appendChild(elementDescriptionInput);

    elementGroup.appendChild(elementPhotoGroup);
    elementGroup.appendChild(elementDescriptionGroup);

    let elementDeleteButton = document.createElement('button');
    elementDeleteButton.className = 'btn btn-outline-danger border border-start-0';
    elementDeleteButton.type = 'button';
    elementDeleteButton.addEventListener('click', foo => deleteElement(elementInputGroup));
    
    let elementButtonIcon = document.createElement('i');
    elementButtonIcon.className = 'fa-solid fa-xmark';

    elementDeleteButton.appendChild(elementButtonIcon);

    elementInputGroup.appendChild(elementGrab);
    elementInputGroup.appendChild(elementGroup);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addCode() {
    let container = document.createElement('div');
    container.className = 'code sortable-item mt-3 mb-3';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group w-100 d-flex flex-nowrap';

    let elementGrab = document.createElement('span');
    elementGrab.className = 'input-group-text bg-transparent drag-handle border-end-0';

    let elementGrabIcon = document.createElement('i');
    elementGrabIcon.className = 'fa-solid fa-bars';

    elementGrab.appendChild(elementGrabIcon);

    let elementSpan = document.createElement('span');
    elementSpan.className = 'input-group w-25';

    let elementSelect = document.createElement('select');
    elementSelect.className = 'language form-select rounded-0';
    
    let options = [
        {'value': 'py', 'text': 'Python'},
        {'value': 'c', 'text': 'C'},
        {'value': 'cpp', 'text': 'C++'},
        {'value': 'rust', 'text': 'Rust'},
        {'value': 'java', 'text': 'Java'},
        {'value': 'cs', 'text': 'C#'},
        {'value': 'rb', 'text': 'Ruby'},
        {'value': 'go', 'text': 'Go'},
        {'value': 'html', 'text': 'HTML'},
        {'value': 'css', 'text': 'CSS'},
        {'value': 'js', 'text': 'JavaScript'},
        {'value': 'ts', 'text': 'TypeScript'},
        {'value': 'php', 'text': 'PHP'},
        {'value': 'swift', 'text': 'Swift'},
        {'value': 'kt', 'text': 'Kotlin'},
        {'value': 'dart', 'text': 'Dart'},
        {'value': 'sql', 'text': 'SQL'},
        {'value': 'plsql', 'text': 'PL/SQL'},
        {'value': 'json', 'text': 'JSON'},
        {'value': 'xml-doc', 'text': 'XML'},
        {'value': 'yaml', 'text': 'YAML'},
        {'value': 'http', 'text': 'HTTP'},
        {'value': 'sh', 'text': 'BashShell'},
    ]

    for (var element of options) {
        var option = document.createElement('option');
        option.value = element.value;
        option.text = element.text;
        elementSelect.appendChild(option);
    }

    elementSpan.appendChild(elementSelect);

    let elementTextarea = document.createElement('textarea');
    elementTextarea.className = 'content form-control';
    elementTextarea.placeholder = 'Код';
    elementTextarea.minLength = '1';
    elementTextarea.maxLength = '15000';

    let elementDeleteButton = document.createElement('button');
    elementDeleteButton.className = 'btn btn-outline-danger border';
    elementDeleteButton.type = 'button';
    elementDeleteButton.addEventListener('click', foo => deleteElement(elementInputGroup));
    
    let elementButtonIcon = document.createElement('i');
    elementButtonIcon.className = 'fa-solid fa-xmark';

    elementDeleteButton.appendChild(elementButtonIcon);

    elementInputGroup.appendChild(elementGrab);
    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementTextarea);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addPass() {
    let container = document.createElement('div');
    container.className = 'pass sortable-item mt-3 mb-3';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group w-100 d-flex flex-nowrap';

    let elementGrab = document.createElement('span');
    elementGrab.className = 'input-group-text bg-transparent drag-handle border-end-0';

    let elementGrabIcon = document.createElement('i');
    elementGrabIcon.className = 'fa-solid fa-bars';

    elementGrab.appendChild(elementGrabIcon);

    let elementSpan = document.createElement('span');
    elementSpan.className = 'input-group-text bg-transparent flex-grow-1 justify-content-center';

    let elementSpanIcon = document.createElement('i');
    elementSpanIcon.className = 'fa-solid fa-ellipsis';

    elementSpan.appendChild(elementSpanIcon);

    let elementDeleteButton = document.createElement('button');
    elementDeleteButton.className = 'btn btn-outline-danger border';
    elementDeleteButton.type = 'button';
    elementDeleteButton.addEventListener('click', foo => deleteElement(elementInputGroup));
    
    let elementButtonIcon = document.createElement('i');
    elementButtonIcon.className = 'fa-solid fa-xmark';

    elementDeleteButton.appendChild(elementButtonIcon);

    elementInputGroup.appendChild(elementGrab);
    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addTopic() {
    let container = document.getElementById('articleTopics');
    let topicSelect = document.getElementById('articleTopicSelect');
    let topicOptions = topicSelect.options;

    if (!topicSelect.value) {
        return 0;
    }

    let topicId = topicSelect.value;
    let topicName;

    for (var element in topicOptions) {
        if (topicOptions[element].value === topicId) {
            topicName = topicOptions[element].innerHTML;
            topicOptions[element].remove();
            break;
        }
    }

    let topicContainer = document.createElement('li');
    topicContainer.className = 'topic list-group-item d-flex pt-0 pb-0 pe-0';
    topicContainer.id = topicId;
    
    let topicSpan = document.createElement('span');
    topicSpan.className = 'flex-grow-1 d-flex align-items-center';
    topicSpan.innerHTML = topicName;

    let topicDeleteButton = document.createElement('button');
    topicDeleteButton.className = 'btn btn-outline-danger border-0 border-start rounded-start-0';
    topicDeleteButton.type = 'button';
    topicDeleteButton.addEventListener('click', foo => deleteTopic(topicContainer, topicId, topicName));
    
    let topicButtonIcon = document.createElement('i');
    topicButtonIcon.className = 'fa-solid fa-xmark';

    topicDeleteButton.appendChild(topicButtonIcon);

    topicContainer.appendChild(topicSpan);
    topicContainer.appendChild(topicDeleteButton);
    
    container.appendChild(topicContainer);
}

function deleteTopic(topicContainer, topicId, topicName) {
    if (!topicContainer) {
        alert('Щось пішло не так! Спробуйте ще раз');
        return 0;
    }

    let topicSelect = document.getElementById('articleTopicSelect');

    let topicOption = document.createElement('option');
    topicOption.value = topicId;
    topicOption.innerHTML = topicName;

    topicSelect.appendChild(topicOption);

    topicContainer.remove();
}

function setTitlePreview() {
    const title = document.getElementById('title').value;

    let articleTitlePreview = document.getElementById('articleTitlePreview');

    if (title) {
        if (articleTitlePreview.classList.contains('text-danger')) {
            articleTitlePreview.classList.remove('text-danger');
        }

        articleTitlePreview.innerHTML = title;

    } else {
        if (!articleTitlePreview.classList.contains('text-danger')) {
            articleTitlePreview.classList.add('text-danger');
        }

        articleTitlePreview.innerHTML = 'Будь ласка введіть заголовок в конструкторі';
    }
}

function postPublication() {
    const title = document.getElementById('title').value.trim();
    const articleStatus = document.getElementById('articleStatus').value;
    const public = (articleStatus === 'true') ? true : false;

    if (!title) {
        let closeButtom = document.getElementById('closeButton');
        closeButtom.click();
        alert('Заголовок повинен містити щонайменше одну букву! Будь ласка введіть заголовок статті');
        return 0;
    }

    let photos = [];

    let article = {
        'title': title,
        'public': public,
        'content': [],
        'photos': [],
        'body': []
    }

    let photoID = 1;
    let subtitleID = 1;

    let articleElements = document.getElementsByClassName('article')[0].children;

    if (articleElements.length < 1) {
        alert('Стаття не може бути пустою! Будь ласка заповніть її');
        let closeButtom = document.getElementById('closeButton');
        closeButtom.click();
        return 0;
    }
    
    for (let articleElement of articleElements) {
        const type = articleElement.classList[0];

        if (type === 'article-title') {
            continue;
        }

        let elementBody, photoFile;
        switch (type) {
            case 'subtitle':
                elementBody = getSubtitle(articleElement.children[0], subtitleID);
                break;
            case 'text':
                elementBody = getText(articleElement.children[0]);
                break;
            case 'hyperlink':
                elementBody = getHyperlink(articleElement.children[0]);
                break;
            case 'textarea':
                elementBody = getTextarea(articleElement.children[0]);
                break;
            case 'photo':
                let photoBody = getPhoto(articleElement.children[0], photoID);
                elementBody = photoBody[0];
                photoFile = photoBody[1];
                break;
            case 'code':
                elementBody = getCode(articleElement.children[0]);
                break;
            case 'pass':
                elementBody = getPass();
                break;
            default:
                alert('Щось пішло не так! Спробуйте ще раз');
                return 0;
        }

        if (!elementBody) {
            let closeButtom = document.getElementById('closeButton');
            closeButtom.click();
            return 0;
        }

        if (elementBody.type === 'subtitle') {
            let subtitle = {
                'id': subtitleID,
                'content': elementBody.content
            }
            article.content.push(subtitle);
            subtitleID += 1;

        } else if (elementBody.type === 'photo') {
            if (!photoFile) {
                alert('Під час обробки фото файлів щось пішло не так! Спробуйте ще раз');
                return 0;
            }

            let photo = {
                'id': photoID,
                'photo_name': elementBody.photo_name
            }
            article.photos.push(photo);

            photos.push(photoFile);
            photoID += 1;
        }

        article.body.push(elementBody);
    }

    let topicsContainer = document.getElementById('articleTopics').children;

    let topics = [];
    
    for (let topicContainer of topicsContainer) {
        let topic = Number(topicContainer.id);
        topics.push(topic);
    }

    let request = {
        'article': article,
        'topics': topics
    }

    const combinedArticleContent = new FormData();

    for (let i = 0; i < photos.length; i++) {
        photos[i].forEach((value, key) => {
            combinedArticleContent.append(key, value);
        });
    }

    combinedArticleContent.append('json', new Blob([JSON.stringify(request)], { type: 'application/json' }));

    fetch('/articles/builder', {
        method: 'POST',
        body: combinedArticleContent
    })
    .then(response => response.json())
    .then(data => {
        if (data.bad) {
            alert(data.bad);
            return 0;
        }
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.error(error);
    });
}

function getSubtitle(articleElement, subtitleID) {
    let content = articleElement.getElementsByClassName('content')[0].value;

    if (!content) {
        alert('Один підзаголовок пустий! Будь ласка заповніть його');
        return 0;
    }

    let element = {
        'type': 'subtitle',
        'text_type': 'bold',
        'subtitle_id': subtitleID,
        'content': content
    }

    return element;
}

function getText(articleElement) {
    let textType = articleElement.getElementsByClassName('text-type')[0].value;
    let content = articleElement.getElementsByClassName('content')[0].value;

    if (!textType || !content) {
        alert('Один рядок пустий! Будь ласка заповніть його');
        return 0;
    }

    let element = {
        'type': 'text',
        'text_type': textType,
        'content': content
    }

    return element;
}

function getHyperlink(articleElement) {
    let link = articleElement.getElementsByClassName('link')[0].value;
    let content = articleElement.getElementsByClassName('content')[0].value;

    if (!link || !content) {
        alert('Одне гіперпосилання пусте! Будь ласка заповніть його');
        return 0;
    }

    let element = {
        'type': 'hyperlink',
        'text_type': 'link',
        'link': link,
        'content': content
    }

    return element;
}

function getTextarea(articleElement) {
    let textType = articleElement.getElementsByClassName('text-type')[0].value;
    let content = articleElement.getElementsByClassName('content')[0].value;

    if (!textType || !content) {
        alert('Один абзац пустий! Будь ласка заповніть його');
        return 0;
    }

    let element = {
        'type': 'textarea',
        'text_type': textType,
        'content': content
    }

    return element;
}

function getPhoto(articleElement, photoID) {
    let photoElement = articleElement.getElementsByClassName('photo-file')[0];
    let photoFile = photoElement.files[0];

    if (!photoFile) {
        alert('Файл одного фото відсутній! Будь ласка заповніть його');
        return 0;
    }

    let types = ['image/png', 'image/jpg', 'image/jpeg'];

    if (!types.includes(photoFile.type)) {
        alert('Фото профілю повинне бути розширення .png або .jpg');
        return 0;
    }

    if (photoFile.size > 1000 * 1024) {
        alert('Розмір файлу повинен бути не більше ніж 1 мегабайт');
        return 0;
    }

    let photoName = `photo_${photoID}.${photoFile.type.replace(/image\//g, '')}`;

    let photoData = new FormData();
    photoData.append(photoName, photoFile);

    let content = articleElement.getElementsByClassName('content')[0].value;

    let element = {
        'type': 'photo',
        'text_type': 'italic',
        'photo_name': photoName,
        'content': content
    }

    return [element, photoData];
}

function getCode(articleElement) {
    let language = articleElement.getElementsByClassName('language')[0].value;
    let content = articleElement.getElementsByClassName('content')[0].value;

    if (!language || !content) {
        alert('Одне поле з кодом пусте! Будь ласка заповніть його');
        return 0;
    }
    
    let element = {
        'type': 'code',
        'text_type': 'pre',
        'language': language,
        'content': content
    }

    return element;
}

function getPass() {
    let element = {
        'type': 'pass',
        'text_type': 'icon'
    }

    return element;
}

