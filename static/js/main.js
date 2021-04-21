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

