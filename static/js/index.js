const image = document.getElementById("image")
const getImage = () => {
    fetch('/get_image')
        .then(response => response.json())
        .then(response => {
            response = response.base64

            if (!(response === undefined)){
                response.replace("b&#39;", "");
                response.replace("&#39;", "");
                image.src = "data:image/jpg;base64," + response
            }
            return response
        })
}

setInterval(() => {
    getImage()
}, 16);