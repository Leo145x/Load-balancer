let fileInputTag = document.querySelector("#fileUpload");
let messageTag = document.querySelector("#message");

function checkUpload() {
    let file = fileInputTag.files[0];
    if (!file) {
        alert('請選擇檔案');

        return false;
    }

    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
        alert('請上傳 jpeg、png、jpg 圖片');

        return false;
    }

    let message = messageTag.value;
    if (!message) {
        alert('請輸入內容');

        return false;
    }

    return true;
}

function deleteImg() {
    if (confirm("確定要刪除嗎?")) {
        alert("圖文已刪除");
        return true;
    } else {
        return false;
    }
}

// function upload() {
//     let file = fileInputTag.files[0];
//     let message = messageTag.value;
//     console.log(file);
//     console.log(message);
//     // if (file == null) {
//     //     alert("choose file!");
//     //     return;
//     // }
    
//     if (message === "") {
//         alert("input something!");
//         return false;
//     }
//     return true;
// }

// btn.addEventListener("click",async (ele) => {
//     let file = fileInputTag.files[0];
//     let message = messageTag.value;
//     let formData = new FormData();

//     formData.append("file", file);
//     formData.append("message", message);

//     console.log(formData.get("file"));
//     console.log(formData.get("message"));
    // try {
    //     let data = await fetch("/upload", {
    //         method: "POST",
    //         body: formData
    //     });
    //     let response = data.json();
        
    // } catch (error) {
    //     console.error(error);
    // }

    
// })