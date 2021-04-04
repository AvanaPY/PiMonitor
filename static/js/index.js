const image = document.getElementById("image")
let prevID = 0

const updatePage = () => {
    var updateImagePromise = updateImage();
    var timeoutPromise = new Promise(r => setTimeout(r, 20));

    Promise.all([updateImagePromise, timeoutPromise]).then(
        v => updatePage()
    );   
}

const updateImage = async () => {
    if (!document.hidden) {
        var response = await fetch('/api/print?user=emil&pwd=123&data=time:left,image:base64:id',{
            method: 'GET',
        }).then(response => {
            return response.json()
        }).then(response => {
            var b64 = response.data.image.base64;
            b64.replace("b&#39;", "");
            b64.replace("&#39;", "");
            image.src = "data:image/jpg;base64," + b64;

            prevID = response.data.image.id;
        }).catch(error => {
            console.log(`Error: ${error}`)
        });
    }
}

updatePage()