async function get_info_add_dubs() {
    let url = location.pathname + '/' + 'video_info';
    let response = await fetch(url);

    let info = await response.json(); // читаем ответ в формате JSON
    for (let key in info) {
        if (info.hasOwnProperty(key)) {
            let btn = document.createElement('button');
            btn.type = 'button'
            btn.className = 'btn btn-secondary dub-button player-btn'
            btn.innerHTML = key;
            document.getElementById('row_dubs_btn').appendChild(btn)

        }
        add_onclick_dub('dub-button', info)

    }
    let label = document.createElement("div")
    label.innerHTML = 'Озвучка'
    label.className = "text-secondary"
    document.getElementById('row_dubs_btn').before(label)
}

function add_onclick_dub(class_name, info) {
    let elements = document.getElementsByClassName(class_name);
    for (let i = 0; i < elements.length; i++) {
        elements[i].onclick = function () {
            for (let i = 0; i < elements.length; i++) {
                elements[i].className = 'btn btn-secondary dub-button player-btn';

            }
            elements[i].className = 'btn btn-primary dub-button player-btn';
            document.getElementById('row_ep_btn').innerHTML = ''
            if(document.getElementsByClassName('label-ep')[0]){
                document.getElementsByClassName('label-ep')[0].remove()
            }
            load_ep(elements[i].innerHTML, info);

        }

    }

}

function load_ep(dub, info) {
    let eps = info[dub]
    for (let key in eps) {
        if (eps.hasOwnProperty(key)) {
            let btn = document.createElement('button');
            btn.type = 'button'
            btn.className = 'btn btn-secondary ep-button player-btn'
            btn.innerHTML = key;
            document.getElementById('row_ep_btn').appendChild(btn)

        }

    }
    let label = document.createElement("div")
    label.innerHTML = 'Серия'
    label.className = "text-secondary label-ep"
    document.getElementById('row_ep_btn').before(label)
    add_onclick_ep(dub, info)
}

function add_onclick_ep(dub, info) {
    let elements = document.getElementsByClassName('ep-button');
    for (let i = 0; i < elements.length; i++) {
        elements[i].onclick = function () {
            for (let i = 0; i < elements.length; i++) {
                elements[i].className = 'btn btn-secondary ep-button player-btn';

            }
            elements[i].className = 'btn btn-primary ep-button player-btn';
            let ep = info[dub][elements[i].innerHTML]
            let player = new Playerjs({
                id: "player",
                file: location.origin + "/video/" + ep
            });

        }

    }

}

get_info_add_dubs()
