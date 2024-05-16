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
    console.log("data: ", data);
    // console.log("islogin", islogin);
    // console.log("islogin.data", islogin.data);
    // console.log("islogin.data.name", islogin.data.name);
    // console.log("line 84 data: ", data);

    if (data.data && islogin) {
        // console.log("line 87");
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
        // console.log("line 107");
        islogin = islogin["data"]["name"];
        // console.log("line 109 islogin: ", islogin);
        // console.log("line 109 islogin: ", typeof islogin);
        displayNone(islogin);
    }
}
getBookingData();

function displayNone(islogin) {
    mainBefore.style.display = "none";
    mainAfter.style.display = "block";
    // console.log(
    //     "line 118 mainBefore.style.display: ",
    //     mainBefore.style.display
    // );
    // console.log("line 119 mainAfter.style.dispaly: ", mainAfter.style.dispaly);

    footer.style.display = "none";
    footerAfter.style.display = "block";

    let newMessageBlock = document.querySelectorAll(".messageBlock");
    // console.log("line 128 newMessageBlock: ", newMessageBlock);
    // console.log("line 129 newMessageBlock[1]: ", newMessageBlock[1].textContet);
    // console.log(
    //     "line 129 newMessageBlock[1]: typeof",
    //     typeof newMessageBlock[1].textContet
    // );

    newMessageBlock[1].textContent =
        "您好，" + islogin + "，待預定的行程如下 :";
    // console.log("line 134 newMessageBlock[1]: ", newMessageBlock[1]);
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

// order confirm button setting
// disable
const bookingConfirmButton = document.querySelector(".bookingConfirmButton");
function disableBookingConfirmButton() {
    bookingConfirmButton.style.cursor = "default";
    bookingConfirmButton.setAttribute("disabled", true);
}
disableBookingConfirmButton();

// enable confirm button
function enableBookingConfirmButton() {
    bookingConfirmButton.style.cursor = "pointer";
    bookingConfirmButton.style.backgroundColor = "#448899";
    bookingConfirmButton.removeAttribute("disabled");
}

// ====== tappay
TPDirect.setupSDK(
    149909,
    "app_yhT2q7SIMGghOoRAnHp7t8Q9Kf9mOVxQy9MYk28fxiRZdmrmnM7WiDYcnBuB",
    "sandbox"
);

TPDirect.card.setup({
    // Display ccv field
    fields: {
        number: {
            // css selector
            element: "#card-number",
            placeholder: "**** **** **** ****",
        },
        expirationDate: {
            // DOM object
            element: document.getElementById("card-expiration-date"),
            placeholder: "MM / YY",
        },
        ccv: {
            element: "#card-ccv",
            placeholder: "ccv",
        },
    },
    styles: {
        // Style all elements
        input: {
            color: "gray",
        },
        // Styling ccv field
        "input.ccv": {
            // 'font-size': '16px'
        },
        // Styling expiration-date field
        "input.expiration-date": {
            // 'font-size': '16px'
        },
        // Styling card-number field
        "input.card-number": {
            // 'font-size': '16px'
        },
        // style focus state
        ":focus": {
            // 'color': 'black'
        },
        // style valid state
        ".valid": {
            color: "green",
        },
        // style invalid state
        ".invalid": {
            color: "red",
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        "@media screen and (max-width: 400px)": {
            input: {
                color: "orange",
            },
        },
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11,
    },
});

// ====== 實作 TPDirect.card.onUpdate，得知目前卡片資訊的輸入狀態

TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        // submitButton.removeAttribute('disabled')
        enableBookingConfirmButton();
    } else {
        // Disable submit Button to get prime.
        // submitButton.setAttribute('disabled', true)
        console.log('order not work');
    }

    // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay','unknown']
    if (update.cardType === "visa") {
        // Handle card type visa.
    }

    // number 欄位是錯誤的
    if (update.status.number === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.number === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }

    if (update.status.expiry === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.expiry === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }

    if (update.status.ccv === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.ccv === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }
});

const bookingConnectionErrorMessage = document.querySelector(
    ".bookingConnectionErrorMessage"
);
bookingConfirmButton.addEventListener(
    "click",
    function (event) {
        disableBookingConfirmButton();
        if (!judgeDataIntegrity()) {
            bookingConnectionErrorMessage.style.display = "block";
            bookingConnectionErrorMessage.textContent =
                "聯絡資訊欄位需完整填寫";
            enableBookingConfirmButton();
            return;
        }
        if (!judgeEmailFormal) {
            bookingConnectionErrorMessage.style.display = "block";
            bookingConnectionErrorMessage.textContent =
                "信箱格式有誤，請確認後點擊送出";
            enableBookingConfirmButton();
            return;
        }
        onSubmit(event);
    },
    false
);

// ====== order data check for submit
function judgeDataIntegrity() {
    if (
        bookingName.value !== "" &&
        bookingEmail.value !== "" &&
        bookingCellphone.value !== ""
    ) {
        console.log("order data are not empty");
        return true;
    }
}

// 前端正則表達式
function judgeEmailFormal() {
    let testForEmail = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$/;
    if (testForEmail.test(bookingEmail.value) == true) {
        return true;
    }
}

// call TPDirect.card.getPrime when user submit form to get tappay prime
// $('form').on('submit', onSubmit)

function onSubmit(event) {
    event.preventDefault();

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    console.log("tappayStatus: ", tappayStatus);
    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert("can not get prime");
        return;
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert("get prime error " + result.msg);
            return;
        }
        prime = result.card.prime;
        console.log("prime: ", prime);
        bookingDataFortappay = collectBookingDataForTappay(prime);
        console.log("bookingDataFortappay: ", bookingDataFortappay);
        postBookingDataForTappayToBackend(bookingDataFortappay);

        // alert("get prime 成功，prime: " + result.card.prime);

        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    });
}

function collectBookingDataForTappay(prime) {
    dataForTappay = {
        prime: prime,
        order: {
            price: bookingTotalPrice.textContent,
            trip: {
                attraction: {
                    id: trashcan.id,
                    name: attractionNameContent.textContent,
                    address: orderAddressContent.textContent,
                    image: imageBlock.src,
                },
                date: orderDateContent.textContent,
                time: orderTimeContent.textContent,
            },
            contact: {
                name: bookingName.value,
                email: bookingEmail.value,
                phone: bookingCellphone.value,
            },
        },
    };
    return dataForTappay;
}

function postBookingDataForTappayToBackend(bookingDataFortappay) {
    let token = localStorage.getItem("token");
    fetch("/api/orders", {
        method: "POST",
        body: JSON.stringify(bookingDataFortappay),
        headers: {
            "content-type": "application/json",
            authorization: `Bearer ${token}`,
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log("orders: ", data);
            if (data.error) {
                alert("付款失敗，" + data["message"]);
            } else {
                if (data["data"]["payment"]["status"] === 0) {
                    let orderNumber = data["data"]["number"];
                    alert(`訂單編號${orderNumber}預訂成功`);
                    window.location.href = `/thankyou?number=${orderNumber}`;
                } else {
                    alert(
                        `訂單編號${data["data"]["number"]}付款失敗，錯誤代碼為${data["data"]["payment"]["status"]}，請重新預訂`
                    );
                    window.location.href = "/";
                }
            }
        });
}
