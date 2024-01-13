document.addEventListener('DOMContentLoaded', function () {
      var helpModalButton = document.getElementById('helpModalButton');
      helpModalButton.click();
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
    container.className = 'subtitle';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group mt-3 mb-3 w-100';

    let elementSpan = document.createElement('span');
    elementSpan.className = 'input-group-text bg-transparent w-25';
    elementSpan.innerHTML = 'Підзаголовок';

    let elementInput = document.createElement('input');
    elementInput.className = 'form-control';
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

    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementInput);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addText() {
    let container = document.createElement('div');
    container.className = 'text';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group mt-3 mb-3 w-100';

    let elementSpan = document.createElement('span');
    elementSpan.className = 'w-25';

    let elementSelect = document.createElement('select');
    elementSelect.className = 'form-select rounded-start rounded-0';
    
    let options = [
        {'value': 'paragraph', 'text': 'Звичайний'},
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
    elementInput.className = 'form-control';
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

    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementInput);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addHyperlink() {
    let container = document.createElement('div');
    container.className = 'hyperlink';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group mt-3 mb-3 w-100 d-flex flex-nowrap';

    let elementGroup = document.createElement('div');
    elementGroup.className = 'w-auto flex-grow-1';

    let elementLinkGroup = document.createElement('div');
    elementLinkGroup.className = 'input-group w-100';

    let elementLinkSpan = document.createElement('span');
    elementLinkSpan.className = 'input-group-text bg-transparent w-25 rounded-0 rounded-top rounded-end-0 border-bottom-0';
    elementLinkSpan.innerHTML = 'Посилання';

    let elementLinkInput = document.createElement('input');
    elementLinkInput.className = 'form-control rounded-0 border-bottom-0';
    elementLinkInput.type = 'text';
    elementLinkInput.placeholder = 'Посилання';
    elementLinkInput.minLength = '1';
    elementLinkInput.maxLength = '200';

    elementLinkGroup.appendChild(elementLinkSpan);
    elementLinkGroup.appendChild(elementLinkInput);

    let elementSignGroup = document.createElement('div');
    elementSignGroup.className = 'input-group w-100';

    let elementSignSpan = document.createElement('span');
    elementSignSpan.className = 'input-group-text bg-transparent w-25 rounded-end-0 rounded-top-0';
    elementSignSpan.innerHTML = 'Підпис';

    let elementSignInput = document.createElement('input');
    elementSignInput.className = 'form-control rounded-0';
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

    elementInputGroup.appendChild(elementGroup);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addTextarea() {
    let container = document.createElement('div');
    container.className = 'textarea';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group mt-3 mb-3 w-100';

    let elementSpan = document.createElement('span');
    elementSpan.className = 'input-group w-25';

    let elementSelect = document.createElement('select');
    elementSelect.className = 'form-select rounded-start rounded-0';
    
    let options = [
        {'value': 'paragraph', 'text': 'Звичайний'},
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
    elementTextarea.className = 'form-control';
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

    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementTextarea);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addPhoto() {
    let container = document.createElement('div');
    container.className = 'photo';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group mt-3 mb-3 w-100 d-flex flex-nowrap';

    let elementGroup = document.createElement('div');
    elementGroup.className = 'w-auto flex-grow-1';

    let elementPhotoGroup = document.createElement('div');
    elementPhotoGroup.className = 'input-group w-100';

    let elementPhotoSpan = document.createElement('span');
    elementPhotoSpan.className = 'input-group-text bg-transparent w-25 rounded-0 rounded-top rounded-end-0 border-bottom-0';
    elementPhotoSpan.innerHTML = 'Фото';

    let elementPhotoInput = document.createElement('input');
    elementPhotoInput.className = 'form-control rounded-0 border-bottom-0';
    elementPhotoInput.type = 'file';

    elementPhotoGroup.appendChild(elementPhotoSpan);
    elementPhotoGroup.appendChild(elementPhotoInput);

    let elementDescriptionGroup = document.createElement('div');
    elementDescriptionGroup.className = 'input-group w-100';

    let elementDescriptionSpan = document.createElement('span');
    elementDescriptionSpan.className = 'input-group-text bg-transparent w-25 rounded-end-0 rounded-top-0';
    elementDescriptionSpan.innerHTML = 'Опис';

    let elementDescriptionInput = document.createElement('input');
    elementDescriptionInput.className = 'form-control rounded-0';
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

    elementInputGroup.appendChild(elementGroup);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addCode() {
    let container = document.createElement('div');
    container.className = 'code';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group mt-3 mb-3 w-100';

    let elementSpan = document.createElement('span');
    elementSpan.className = 'input-group w-25';

    let elementSelect = document.createElement('select');
    elementSelect.className = 'form-select rounded-start rounded-0';
    
    let options = [
        {'value': '', 'text': 'Python'},
        {'value': '', 'text': 'C'},
        {'value': '', 'text': 'C++'},
        {'value': '', 'text': 'Rust'},
        {'value': '', 'text': 'Java'},
        {'value': '', 'text': 'C#'},
        {'value': '', 'text': 'Ruby'},
        {'value': '', 'text': 'Go'},
        {'value': '', 'text': 'HTML'},
        {'value': '', 'text': 'CSS'},
        {'value': '', 'text': 'JavaScript'},
        {'value': '', 'text': 'TypeScript'},
        {'value': '', 'text': 'SQL'},
        {'value': '', 'text': 'Swift'},
        {'value': '', 'text': 'Kotlin'},
        {'value': '', 'text': 'Flutter'}
    ]

    for (var element of options) {
        var option = document.createElement('option');
        option.value = element.value;
        option.text = element.text;
        elementSelect.appendChild(option);
    }

    elementSpan.appendChild(elementSelect);

    let elementTextarea = document.createElement('textarea');
    elementTextarea.className = 'form-control';
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

    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementTextarea);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);

    return container;
}

function addPass() {
    let container = document.createElement('div');
    container.className = 'pass';

    let elementInputGroup = document.createElement('div');
    elementInputGroup.className = 'input-group mt-3 mb-3 w-100';

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

    elementInputGroup.appendChild(elementSpan);
    elementInputGroup.appendChild(elementDeleteButton);

    container.appendChild(elementInputGroup);
    console.log(container);
    return container;
}
