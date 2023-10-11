// ====== 取得訂單
(function showOrderId() {
    let urlParams = new URLSearchParams(window.location.search);
    let order_id = urlParams.get("number");
    let orderIdElem = document.querySelector("#orderId");
    orderIdElem.textContent = `訂單編號：${order_id}`;
})();

let nameBlock = document.querySelector(".nameBlock");
let emailBlock = document.querySelector(".emailBlock");
let phoneBlock = document.querySelector(".phoneBlock");
let dateBlock = document.querySelector(".dateBlock");
let timeBlock = document.querySelector(".timeBlock");
let priceBlock = document.querySelector(".priceBlock");

// console.log(orderUrl);
let orderUrl = "/api/order/" + window.location.search.replace("?number=", "");
function getDataFromOrdersUrl(orderUrl) {
    let token = localStorage.getItem("token");

    fetch(orderUrl, {
        method: "GET",
        headers: {
            authorization: `Bearer ${token}`,
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.data) {
                nameBlock.textContent = `姓名：${data.data.contact.name}`;
                emailBlock.textContent = `信箱：${data.data.contact.email}`;
                phoneBlock.textContent = `電話：${data.data.contact.phone}`;
                dateBlock.textContent = `日期：${data.data.trip.date}`;
                timeBlock.textContent = `時間：${data.data.trip.time}`;
                priceBlock.textContent = `費用：新台幣${data.data.price}元`;
            } else {
                alert("訂單錯誤");
                // window.location.href = "/";
            }
        });
}
getDataFromOrdersUrl(orderUrl);
