// ====== 取得訂單
(function showOrderId() {
    const urlParams = new URLSearchParams(window.location.search);
    const order_id = urlParams.get("number");
    let orderIdElem = document.querySelector("#orderId");
    orderIdElem.textContent = order_id;
})();
