const nav_home = document.querySelector(".nav_home");
nav_home.addEventListener("click", (event) => {
    let url = "/";
    window.location.href = url;
});

const signinRegisterBtn = document.querySelector(".signin_register_btn");

const filmBackground = document.querySelector(".filmBackground");

const signinBlock = document.querySelector(".signinBlock");
const signinCreateAccount = document.querySelector(".signinCreateAccount");
const signinContent = document.querySelector(".signinContent");

const registerBlock = document.querySelector(".registerBlock");
const registerSignInTo = document.querySelector(".registerSignInTo");
const registerContent = document.querySelector(".registerContent");

const signinClose = document.querySelector(".signinClose");
const registerClose = document.querySelector(".registerClose");

const registerMessage = document.querySelector(".registerMessage");
const signinMessage = document.querySelector(".signinMessage");

const signin_register_btn = document.querySelector(".signin_register_btn");
const signout_btn = document.querySelector(".signout_btn");

signinRegisterBtn.addEventListener(
    "click",
    function () {
        filmBackground.style.display = "flex";
        signinBlock.style.display = "block";
    },
    false
);
// console.log("user.js");
signinCreateAccount.addEventListener("click", function () {
    registerBlock.style.display = "block";
    signinBlock.style.display = "none";
    signinBlock.style.height = "275px";
    signinContent.style.height = "235px";
    signinMessage.style.display = "none";
    document.querySelector(".signinEmail").value = "";
    document.querySelector(".signinPassword").value = "";
    document.querySelector(".registerName").value = "";
    document.querySelector(".registerEmail").value = "";
    document.querySelector(".registerPassword").value = "";
});

registerSignInTo.addEventListener("click", function () {
    registerBlock.style.display = "none";
    signinBlock.style.display = "block";
    registerBlock.style.height = "332px";
    registerContent.style.height = "302px";
    registerMessage.style.display = "none";
    document.querySelector(".signinEmail").value = "";
    document.querySelector(".signinPassword").value = "";
    document.querySelector(".registerName").value = "";
    document.querySelector(".registerEmail").value = "";
    document.querySelector(".registerPassword").value = "";
});

signinClose.addEventListener(
    "click",
    function () {
        modalClose();
    },
    false
);
registerClose.addEventListener(
    "click",
    function () {
        modalClose();
    },
    false
);

function modalClose() {
    signinBlock.style.display = "none";
    registerBlock.style.display = "none";
    filmBackground.style.display = "none";
    signinMessage.style.display = "none";
    registerMessage.style.display = "none";
    signinBlock.style.height = "275px";
    signinContent.style.height = "235px";
    registerBlock.style.height = "332px";
    registerContent.style.height = "302px";

    document.querySelector(".signinEmail").value = "";
    document.querySelector(".signinPassword").value = "";
    document.querySelector(".registerName").value = "";
    document.querySelector(".registerEmail").value = "";
    document.querySelector(".registerPassword").value = "";
}

// ====== registerData
let registerData = {};
const registerBtn = document.querySelector(".registerBtn");
registerBtn.addEventListener(
    "click",
    function () {
        registerName = document.querySelector(".registerName").value;
        registerEmail = document.querySelector(".registerEmail").value;
        registerPassword = document.querySelector(".registerPassword").value;
        registerData = {
            name: registerName,
            email: registerEmail,
            password: registerPassword,
        };
        checkRegisterFront(registerName, registerEmail, registerPassword);
    },
    false
);

// front end check data
function checkRegisterFront(registerName, registerEmail, registerPassword) {
    console.log("check front end");
    let testForEmail = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$/;
    // let testForEmail = /.+@.+\..+/;
    console.log(testForEmail.test(registerEmail));
    console.log(registerEmail);
    console.log(registerName);
    console.log(registerPassword);

    if (
        registerEmail !== "" &&
        registerName !== "" &&
        registerPassword !== ""
    ) {
        if (testForEmail.test(registerEmail) === true) {
            console.log("pass front end");
            postRegisterDataToBackEnd();
        } else if (testForEmail.test(registerEmail) !== true) {
            responseFromBackEnd = { message: "Email格式錯誤" };
            dealRegisterResponseFromBackEnd();
        }
    } else {
        responseFromBackEnd = { message: "註冊欄位需全部填寫" };
        dealRegisterResponseFromBackEnd();
    }
}

// POST to backend for /api/user
let responseFromBackEnd = "";
function postRegisterDataToBackEnd() {
    fetch("/api/user", {
        method: "POST",
        body: JSON.stringify(registerData),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            responseFromBackEnd = data;
            dealRegisterResponseFromBackEnd();
        });
}

// refresh fornt web page
function dealRegisterResponseFromBackEnd() {
    registerMessage.style.display = "block";
    registerBlock.style.height = "355px";
    registerContent.style.height = "325px";
    if (responseFromBackEnd.ok === true) {
        registerMessage.textContent = "註冊成功";
        registerMessage.style.color = "green";
        document.querySelector(".registerName").value = "";
        document.querySelector(".registerEmail").value = "";
        document.querySelector(".registerPassword").value = "";
        // setTimeout(function () {
        //     modalClose();
        //     filmBackground.style.display = "flex";
        //     registerBlock.style.display = "block";
        // }, 1000);
    } else {
        registerMessage.textContent = responseFromBackEnd.message;
        document.querySelector(".registerName").value = "";
        document.querySelector(".registerEmail").value = "";
        document.querySelector(".registerPassword").value = "";
        registerMessage.addEventListener("click", function () {
            modalClose();
            filmBackground.style.display = "flex";
            registerBlock.style.display = "block";
            // setTimeout(function () {
            //     modalClose();
            //     filmBackground.style.display = "flex";
            //     registerBlock.style.display = "block";
            // }, 1000);
            // document.querySelector(".registerName").value = "";
            // document.querySelector(".registerEmail").value = "";
            // document.querySelector(".registerPassword").value = "";
            // registerMessage.style.display = "none";
            // registerBlock.style.height = "355px";
            // registerContent.style.height = "325px";
        });
    }
}

// get signin data
let signinEmail = "";
let signinPassword = "";
let signinData = {};
const signinBtn = document.querySelector(".signinBtn");
signinBtn.addEventListener(
    "click",
    function () {
        signinEmail = document.querySelector(".signinEmail").value;
        signinPassword = document.querySelector(".signinPassword").value;
        signinData = { email: signinEmail, password: signinPassword };
        pushSigninDataToBackEnd();
    },
    false
);

function pushSigninDataToBackEnd() {
    fetch("/api/user/auth", {
        method: "PUT",
        body: JSON.stringify(signinData),
        headers: { "content-type": "application/json" },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            localStorage.setItem("token", data.token);
            responseFromBackEnd = data;
            dealSigninResponseFromBackEnd();
            checkUserToken();
        });
}

function dealSigninResponseFromBackEnd() {
    if (responseFromBackEnd.token) {
        signin_register_btn.style.display = "none";
        signout_btn.style.display = "block";
        modalClose();
    } else {
        signinMessage.style.display = "block";
        signinBlock.style.height = "298px";
        signinContent.style.height = "258px";
        signinMessage.textContent = responseFromBackEnd.message;
        signinMessage.addEventListener("click", function () {
            modalClose();
            filmBackground.style.display = "flex";
            signinBlock.style.display = "block";
        });
    }
}

window.addEventListener("load", function () {
    checkToken();
});

function checkUserToken() {
    if (localStorage.getItem("token")) {
        let url = "/api/user/auth";
        let token = localStorage.getItem("token");
        fetch(url, {
            method: "GET",
            headers: { authorization: `Bearer ${token}` },
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data["data"] != null) {
                    signin_register_btn.style.display = "none";
                    signout_btn.style.display = "block";
                    let url = "/booking";
                    window.location.href = url;
                } else {
                    signout();
                    return false;
                }
            });
    } else {
        signout();
        return false;
    }
}

function checkToken() {
    if (localStorage.getItem("token")) {
        let url = "/api/user/auth";
        let token = localStorage.getItem("token");
        fetch(url, {
            method: "GET",
            headers: { authorization: `Bearer ${token}` },
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data["data"] != null) {
                    signin_register_btn.style.display = "none";
                    signout_btn.style.display = "block";
                    return data;
                } else {
                    signout();
                    return false;
                }
            });
    } else {
        signout();
        return false;
    }
}

// ====== async_checkToken

function async_checkToken() {
    return new Promise((resolve, reject) => {
        if (localStorage.getItem("token")) {
            let url = "/api/user/auth";
            let token = localStorage.getItem("token");
            fetch(url, {
                method: "GET",
                headers: { authorization: `Bearer ${token}` },
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (data["data"] != null) {
                        signin_register_btn.style.display = "none";
                        signout_btn.style.display = "block";
                        resolve(data);
                    } else {
                        signout();
                        resolve(false);
                    }
                })
                .catch(function (error) {
                    reject(error);
                });
        } else {
            signout();
            resolve(false);
        }
    });
}

// ====== signout
function signout() {
    localStorage.removeItem("token");
    signin_register_btn.style.display = "block";
    signout_btn.style.display = "none";
}

signout_btn.addEventListener("click", function () {
    signout();
    modalClose();
    let url = "/";
    window.location.href = url;
});

// ====== booking
const goToBooking = document.querySelector(".nav_button");
goToBooking.addEventListener("click", function () {
    if (localStorage.getItem("token")) {
        let url = "/api/user/auth";
        let token = localStorage.getItem("token");
        fetch(url, {
            method: "GET",
            headers: { authorization: `Bearer ${token}` },
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data["data"] != null) {
                    let url = "/booking";
                    window.location.href = url;
                } else {
                    signout();
                    filmBackground.style.display = "flex";
                    signinBlock.style.display = "block";
                }
            });
    } else {
        signout();
        filmBackground.style.display = "flex";
        signinBlock.style.display = "block";
    }
});
