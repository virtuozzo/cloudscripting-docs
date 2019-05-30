var feedback = {};

(function(config) {
    var BODY = "body",
        oBody,
        oWrapper,
        oTextArea,
        oSendBtn,
        sSelection,
        oDescription;

    $(BODY).ready(function () {
        var NOT_VISIBLE = "not-visible",
            DISABLE = "disable";

        config.body = oBody = $(BODY);
        config.wrapper = oWrapper = $(".wrapper");
        config.popupContent = oWrapper.children(":first");
        config.description = oDescription = oWrapper.find(".popup-description");
        config.textarea = oTextArea = config.popupContent.find(".comment");
        config.selectedText = oDescription.find(".selected .text");
        config.sendBtn = oSendBtn = config.popupContent.find('.actions .btn');
        config.successForm = config.popupContent.find(".successText");
        config.username = config.popupContent.find(".name .input");

        config.textarea.keyup(enableSendBtn).focusout(enableSendBtn);

        config.body.keypress(function (e) {
            if (e.ctrlKey && (e.keyCode == 10 || e.keyCode == 13)) {
                sSelection = window.getSelection().toString() || "";
                config.wrapper.removeClass(NOT_VISIBLE);

                if (sSelection) {
                    config.sendBtn.removeClass(DISABLE);
                    config.description.removeClass(NOT_VISIBLE);
                    config.selectedText.text(sSelection);
                } else {
                    config.sendBtn.addClass(DISABLE);
                    config.description.addClass(NOT_VISIBLE);
                }
            }
        });
        config.body.keyup(function(e) {
            if (e.keyCode == 27) {
                config.wrapper.addClass(NOT_VISIBLE);
            }
        });

        function enableSendBtn() {
            if (!this.value) {
                config.sendBtn.addClass(DISABLE);
            } else {
                config.sendBtn.removeClass(DISABLE);
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
        url = window.location.protocol + "//" + window.location.hostname + "/issue_report.php",//"http://docs.cloudscripting.local/issue_report.php",
        nTopPosition = window.getSelection().getRangeAt(0).getBoundingClientRect().top + window.pageYOffset,
        sComment = feedback.textarea.val() || "",
        sSelected = feedback.selectedText.text() || "",
        oSelectedAnchorNode = window.getSelection().anchorNode,
        sSelectedParent = oSelectedAnchorNode.parentElement,
        sUserName = feedback.username.val() || "",
        params;

    while (sSelectedParent.outerText.length <= sSelected.length) {
        sSelectedParent = sSelectedParent.parentElement;
    }

    params = encodeURI("comment=" + sComment + "&selected=" + sSelected + "&page=" + window.location.pathname + "&userName=" + sUserName + "&parent=" + sSelectedParent.outerText);

    //TODO add userName page
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');//application/json//application/x-www-form-urlencoded
    xhr.send(params);
    showSuccess();
    feedback.textarea.val();
}

function showSuccess() {
    feedback.successForm = $(".successText");
    feedback.popupContent = $(".popup-content");
    feedback.popupContent.hide();
    feedback.successForm.removeClass("not-visible");

    setTimeout(function() {
        closeSendContent();
    }, 3000);
}