const image = document.getElementById("image")
const getImage = () => {
    fetch('/get_image')
        .then(response => response.json())
        .then(response => {
            response = response.base64
            response.replace("b&#39;", "");
            response.replace("&#39;", "");
            return response;
        })
        .then(response => {
            image.src = "data:image/jpg;base64," + response
        });
}

setInterval(() => {
    getImage()
}, 16);