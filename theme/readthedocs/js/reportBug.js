var feedback = {};

(function(config) {
    var BODY = "body",
        oBody,
        oWrapper,
        oTextArea,
        oSendBtn,
        sSelection,
        oSelection,
        oDescription;

    $(BODY).ready(function () {
        var NOT_VISIBLE = "not-visible",
            DISABLE = "disable";

        config.body = oBody = $(BODY);
        config.gridBody = oBody.children('.wy-grid-for-nav');
        config.wrapper = oWrapper = $(".wrapper");
        config.popupContent = oWrapper.children(":first");
        config.description = oDescription = oWrapper.find(".popup-description");
        config.textarea = oTextArea = config.popupContent.find(".comment");
        config.note = config.popupContent.find(".rst-content");
        config.selectedText = oDescription.find(".selected .text");
        config.selectedParent= "";
        config.sendBtn = oSendBtn = config.popupContent.find('.actions .btn');
        config.successForm = config.popupContent.find(".successText");
        config.username = config.popupContent.find(".name .input");

        config.textarea.keyup(enableSendBtn).focusout(enableSendBtn);

        /*
        test scroll
         */
        function preventDefault(e) {
            if (!config.wrapper.hasClass(NOT_VISIBLE)) {
                e = e || window.event;
                if (e.preventDefault)
                    e.preventDefault();
                e.returnValue = false;
            }
        }
        window.addEventListener('DOMMouseScroll', preventDefault, false);
        window.onwheel = preventDefault; // modern standard
        window.onmousewheel = document.onmousewheel = preventDefault; // older browsers, IE
        window.ontouchmove  = preventDefault;

        config.body.keypress(function (e) {
            if (e.ctrlKey && (e.keyCode == 10 || e.keyCode == 13)) {

                if (!config.wrapper.hasClass(NOT_VISIBLE)) return;

                oSelection = window.getSelection();
                sSelection = oSelection.toString() || "";
                config.selectedParent = oSelection.anchorNode;
                config.wrapper.removeClass(NOT_VISIBLE);

                if (config.username.val()) {
                    config.textarea.focus();
                } else {
                    config.username.focus();
                }

                if (sSelection) {
                    config.sendBtn.removeClass(DISABLE);
                    config.description.removeClass(NOT_VISIBLE);
                    config.selectedText.text(sSelection);
                    config.note.addClass(NOT_VISIBLE);
                } else {
                    if (!config.textarea.val()) {
                        config.sendBtn.addClass(DISABLE);
                    }
                    config.note.removeClass(NOT_VISIBLE);
                    config.description.addClass(NOT_VISIBLE);
                }
            }
        });

        config.body.keyup(function(e) {
            if (e.keyCode == 27) {
                config.wrapper.addClass(NOT_VISIBLE);
            }
        });

        config.body.on('click', function(event) {
            if (!config.wrapper.hasClass(NOT_VISIBLE) && !config.popupContent.has(event.target).length) {
                config.wrapper.addClass(NOT_VISIBLE);
            }
        });

        function enableSendBtn() {
            if (!this.value.trim()) {
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
        url = window.location.protocol + "//" + window.location.hostname + "/issue_report.php",
        sComment = feedback.textarea.val() || "",
        sSelected = feedback.selectedText.text() || "",
        oSelectedAnchorNode = feedback.selectedParent,//window.getSelection().anchorNode,
        sSelectedParent = oSelectedAnchorNode.parentElement,
        sUserName = feedback.username.val() || "",
        params;

    while (sSelectedParent.outerText.length <= sSelected.length) {
        sSelectedParent = sSelectedParent.parentElement;
    }

    params = encodeURI("comment=" + sComment + "&selected=" + sSelected + "&page=" + window.location.pathname + "&userName=" + sUserName + "&parent=" + sSelectedParent.outerText);

    //TODO add userName page
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(params);
    feedback.textarea.val("");
    feedback.gridBody.removeClass("no-scroll");
    showSuccess();
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