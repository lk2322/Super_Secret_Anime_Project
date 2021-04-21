function validateForm() {
    let x = document.forms["search"]["q"].value;
    if (x == false) {
        return false;
    }
}

async function add_to_favorite() {
    let url = location.pathname + '/' + 'bookmark';
    if (bookmark.innerHTML === 'В закладках') {
        bookmark.className = 'btn btn-primary';
        bookmark.innerHTML = 'Добавить в закладки';
        await fetch(url, {
            method: 'DELETE',
            credentials: 'same-origin'
        })
    } else {
        bookmark.className = 'btn btn-outline-primary';
        bookmark.innerHTML = 'В закладках';
        await fetch(url, {
            method: 'POST',
            credentials: 'same-origin'
        })
    }


}

async function if_in_bookmark() {
    let url = location.pathname + '/' + 'bookmark';
    let response = await fetch(url);
    let bookmark = document.getElementById('bookmark')
    if (response.status === 400) {
        bookmark.className = 'btn btn-outline-primary';
        bookmark.innerHTML = 'В закладках';
    }

}
if_in_bookmark()