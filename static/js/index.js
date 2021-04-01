const image = document.getElementById("image")
let prevID = 0
const getImage = () => {
    var response = fetch('/get_image', {
        method: "GET",
        headers: {
            'Last-Image-ID': prevID
        }
    }).then(response => 
        response.json()
    ).then(response => {
        if (response.status === "ok") {
            var id = response.ID;
            if(id !== prevID) {
                var b64 = response.base64;
                b64.replace("b&#39;", "");
                b64.replace("&#39;", "");
                image.src = "data:image/jpg;base64," + b64;

                prevID = id;
                console.log("new id!");
            }
        }
        return response;
    })

    var timeoutPromise = new Promise(r => setTimeout(r, 20));

    Promise.all([response, timeoutPromise]).then(
        v => getImage()
    );
    
}

getImage()