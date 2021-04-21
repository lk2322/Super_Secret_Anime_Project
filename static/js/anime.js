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