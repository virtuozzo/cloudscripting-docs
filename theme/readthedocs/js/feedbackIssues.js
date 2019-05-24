var feedback = {};

(function(config) {
    var BODY = "body",
        oBody,
        oWrapper,
        oTextArea,
        oSendBtn,
        sSelection;

    $(BODY).ready(function () {
        config.body = oBody = $(BODY);
        config.wrapper = oWrapper = $(".wrapper");
        config.textarea = oTextArea = $(".comment");
        config.sendBtn = oSendBtn = $('.actions .btn');

        config.textarea.keyup(enableSendBtn).focusout(enableSendBtn);

        config.body.keypress(function (e) {
            if (e.ctrlKey && (e.keyCode == 10 || e.keyCode == 13)) {
                sSelection = window.getSelection().toString() || "";
                config.wrapper.removeClass("not-visible");

                if (sSelection) {
                    config.sendBtn.removeClass("disable");
                } else {
                    config.sendBtn.addClass("disable");
                }
                config.textarea.val(sSelection);
            }
        });
        config.body.keyup(function(e) {
            if (e.keyCode == 27) {
                config.wrapper.addClass("not-visible");
            }
        });

        function enableSendBtn() {
            if (!this.value) {
                config.sendBtn.addClass("disable");
            } else {
                config.sendBtn.removeClass("disable");
            }
        }
    });
})(feedback);

function closeSendContent() {
    feedback.successForm.addClass("not-visible");
    feedback.popupContent.show();
    feedback.wrapper.addClass("not-visible");
}

function sendIssue() {
    var xhr = new XMLHttpRequest(),
        token = "48f6b1b14674e92b1de2d85425ba43a599a3bf6c",
        url = "https://api.github.com/repos/dzotic9/docs/issues",
        issueParams;

    issueParams = {
        title: "Issue",
        body: feedback.textarea.val() || "",
        assignee: "dzotic9",
        labels: ["bug", "help wanted"]
    };

    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Authorization', 'token ' + token);

    xhr.send(JSON.stringify(issueParams));
    showSuccess();
}

function showSuccess() {
    var oSuccessForm,
        oPopup;

    feedback.successForm = oSuccessForm = $(".successText");
    feedback.popupContent = oPopup = $(".popup-content");

    oPopup.hide();
    oSuccessForm.removeClass("not-visible");

    setTimeout(function() {
        closeSendContent();
    }, 3000);
}