fetch("https://api.github.com/repos/JohnGrubba/TromboneChampAutomod/commits/main").then((response) => response.json())
    .then((data) => {
        fetch("https://raw.githubusercontent.com/JohnGrubba/TromboneChampAutomod/" + data.sha + "/songs.json")
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                out = "";
                id = 0;
                data.forEach(element => {
                    out += "<li><a class='id'>" + id + "</a><a class='name'>" + element.song_name + "</a><a id='dl' href='" + element.dl + "'>Download</a></li>"
                    id++;
                });
                document.getElementById("songs").innerHTML = out;
            });
    });

function search() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('search');
    filter = input.value.toUpperCase();
    ul = document.getElementById("songs");
    li = ul.getElementsByTagName('li');
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[1];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
    console.log("Filtered" + input.value.toUpperCase())
}