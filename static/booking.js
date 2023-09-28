const messageBlock = document.querySelector(".messageBlock");
const attractionNameContent = document.querySelector(".attractionNameContent");
const orderDateContent = document.querySelector(".orderDateContent");
const orderTimeContent = document.querySelector(".orderTimeContent");
const orderFeeContent = document.querySelector(".orderFeeContent");
const orderAddressContent = document.querySelector(".orderAddressContent");
const imageBlock = document.querySelector(".imageBlock");
const bookingTotalPrice = document.querySelector(".bookingTotalPrice");
const trashcan = document.querySelector(".trashcan");

// function checkBookingToken() {
//     if (localStorage.getItem("token")) {
//         let url = "/api/user/auth";
//         let token = localStorage.getItem("token");
//         fetch(url, {
//             method: "GET",
//             headers: { authorization: `Bearer ${token}` },
//         })
//             .then(function (response) {
//                 return response.json();
//             })
//             .then(function (data) {
//                 if (data["data"] === null) {
//                     let url = "/";
//                     window.location.href = url;
//                 } else {
//                     console.log("/booking auth驗證成功");
//                 }
//             });
//     } else {
//         let url = "/";
//         window.location.href = url;
//     }
// }

//// cancel
// goToBooking.addEventListener("click", async function () {
//     try {
//         const islogin = await checkToken();
//         console.log(islogin);
//         if (islogin) {
//             let url = "/booking";
//             window.location.href = url;
//         } else {
//             filmBackground.style.display = "flex";
//             signinBlock.style.display = "block";
//         }
//     } catch (error) {
//         console.error(error);
//     }
// });
//
window.addEventListener("load", async function () {
    try {
        const islogin = await async_checkToken();
        if (islogin == false) {
            let url = "/";
            window.location.href = url;
        } else {
            console.log("/booking auth驗證成功");
        }
    } catch (error) {
        console.log("booking.js loading error");
    }
});

const bookingName = document.querySelector(".bookingName");
const bookingEmail = document.querySelector(".bookingEmail");
const bookingCellphone = document.querySelector(".bookingCellphone");
let username = "";
async function getBookingData() {
    let token = localStorage.getItem("token");
    let islogin = await async_checkToken();
    let response = await fetch("/api/booking", {
        method: "GET",
        headers: {
            authorization: `Bearer ${token}`,
        },
    });
    const data = await response.json();
    console.log("islogin", islogin);
    console.log("islogin.data", islogin.data);
    console.log("islogin.data.name", islogin.data.name);
    console.log("line 84 data: ", data);

    if (data.data && islogin) {
        console.log("line 87");
        messageBlock.textContent =
            "您好，" + islogin["data"]["name"] + "，待預定的行程如下:";
        bookingName.value = islogin["data"]["name"];
        attractionNameContent.textContent = data["data"]["attraction"]["name"];
        orderDateContent.textContent = data["data"]["date"];
        if (data["data"]["time"] == "morning") {
            orderTimeContent.textContent = "早上 9 點到下午 4 點";
            orderFeeContent.textContent = data["data"]["price"];
            bookingTotalPrice.textContent = data["data"]["price"];
        } else {
            orderTimeContent.textContent = "下午 4 點到晚上 8 點";
            orderFeeContent.textContent = data["data"]["price"];
            bookingTotalPrice.textContent = data["data"]["price"];
        }
        orderAddressContent.textContent = data["data"]["attraction"]["address"];
        imageBlock.setAttribute("src", data["data"]["attraction"]["image"]);

        trashcan.setAttribute("id", data["data"]["attraction"]["id"]);
    } else {
        console.log("line 107");
        islogin = islogin["data"]["name"];
        console.log("line 109 islogin: ", islogin);
        console.log("line 109 islogin: ", typeof islogin);
        displayNone(islogin);
    }
}
getBookingData();

function displayNone(islogin) {
    mainBefore.style.display = "none";
    mainAfter.style.display = "block";
    console.log(
        "line 118 mainBefore.style.display: ",
        mainBefore.style.display
    );
    console.log("line 119 mainAfter.style.dispaly: ", mainAfter.style.dispaly);

    footer.style.display = "none";
    footerAfter.style.display = "block";

    let newMessageBlock = document.querySelectorAll(".messageBlock");
    console.log("line 128 newMessageBlock: ", newMessageBlock);
    console.log("line 129 newMessageBlock[1]: ", newMessageBlock[1].textContet);
    console.log(
        "line 129 newMessageBlock[1]: typeof",
        typeof newMessageBlock[1].textContet
    );

    newMessageBlock[1].textContent =
        "您好，" + islogin + "，待預定的行程如下 :";
    console.log("line 134 newMessageBlock[1]: ", newMessageBlock[1]);
}

trashcan.addEventListener("click", function () {
    attractionId = {
        attractionId: trashcan.getAttribute("id"),
    };
    deleteBooking(attractionId);
});

function deleteBooking(attractionId) {
    let token = localStorage.getItem("token");
    fetch("/api/booking", {
        method: "DELETE",
        body: JSON.stringify(attractionId),
        headers: {
            "content-type": "application/json",
            authorization: `Bearer ${token}`,
        },
    }).then(function (response) {
        getBookingData();
        displayNone();
    });
}

const mainBefore = document.querySelector(".mainBefore");
const mainAfter = document.querySelector(".mainAfter");

const footer = document.querySelector(".footer");
const footerAfter = document.querySelector(".footerAfter");

mainAfter.style.display = "none";
