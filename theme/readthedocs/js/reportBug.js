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
        var NOT_VISIBLE_CLS = "not-visible",
            DISABLE = "disable";

        config.body = oBody = $(BODY);
        config.gridBody = oBody.children('.wy-grid-for-nav');
        config.wrapper = oWrapper = $(".wrapper-send-report");
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
            if (!config.wrapper.hasClass(NOT_VISIBLE_CLS)) {
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

                if (!config.wrapper.hasClass(NOT_VISIBLE_CLS)) return;

                config.popupContent.removeClass(NOT_VISIBLE_CLS);
                oSelection = window.getSelection();
                sSelection = oSelection.toString() || "";
                config.selectedParent = oSelection.anchorNode;
                config.wrapper.removeClass(NOT_VISIBLE_CLS);

                if (config.username.val()) {
                    config.textarea.focus();
                } else {
                    config.username.focus();
                }

                if (sSelection) {
                    config.sendBtn.removeClass(DISABLE);
                    config.description.removeClass(NOT_VISIBLE_CLS);
                    config.selectedText.text(sSelection);
                    config.note.addClass(NOT_VISIBLE_CLS);
                } else {
                    config.note.removeClass(NOT_VISIBLE_CLS);
                    config.description.addClass(NOT_VISIBLE_CLS);
                }

                if (!config.textarea.val()) {
                    config.sendBtn.addClass(DISABLE);
                }
            }
        });

        config.body.keyup(function(e) {
            if (e.keyCode == 27) {
                config.wrapper.addClass(NOT_VISIBLE_CLS);
            }
        });

        config.body.on('click', function(event) {
            if (event.target.className == "wrapper-send-report" &&
                !config.wrapper.hasClass(NOT_VISIBLE_CLS) &&
                config.popupContent.hasClass(NOT_VISIBLE_CLS) &&
                !config.successForm.hasClass(NOT_VISIBLE_CLS) &&
                $('.wy-body-for-nav').has(event.target).length) {
                closeSendContent();
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
    var NOT_VISIBLE_CLS = "not-visible";
    feedback.successForm.addClass(NOT_VISIBLE_CLS);
    feedback.wrapper.addClass(NOT_VISIBLE_CLS);
}

function sendIssue() {
    var xhr = new XMLHttpRequest(),
        url = window.location.protocol + "//" + window.location.hostname + "/issue_report.php",
        sComment = feedback.textarea.val() || "",
        sSelected = feedback.selectedText.text() || "",
        oSelectedAnchorNode = feedback.selectedParent,
        sSelectedParent = oSelectedAnchorNode.parentElement,
        sUserName = feedback.username.val() || "",
        sSurroundEls = "",
        sParent = "",
        aSurroundEls,
        nChildIndex,
        oParent,
        oChildren,
        params;

    sSelectedParent = sSelectedParent.parentElement;
    oParent = $(sSelectedParent) || {};
    oChildren = oParent.children() || {};
    nChildIndex = oChildren.index(feedback.selectedParent.parentElement);

    if (oChildren.length > nChildIndex) {
        aSurroundEls = oChildren.slice(nChildIndex-3 > 0 ? nChildIndex-3 : 0, nChildIndex+3 <= oChildren.length ? nChildIndex+3 : oChildren.length);

        for (var i = 0, n = aSurroundEls.length; i < n; i++) {
            if (aSurroundEls[i].outerText.indexOf(sSelected) != -1) {
                if (aSurroundEls[i].outerText.length > sSelected.length) {
                    sSurroundEls += aSurroundEls[i].outerText.replace(sSelected, '\n```\n' + sSelected + "\n```\n");
                } else {
                    sSurroundEls += "\n```\n" + aSurroundEls[i].outerText + "\n```\n";
                }
            } else {
                sSurroundEls += aSurroundEls[i].outerText + "\n";
            }
        }
    }

    sParent = sSurroundEls || "```" + sSelectedParent.outerText + "```";

    params = encodeURI("comment=" + sComment + "&selected=" + sSelected + "&page=" + window.location.pathname + "&userName=" + sUserName + "&context=" + sParent);

    //TODO add userName page
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(params);
    feedback.textarea.val("");
    feedback.gridBody.removeClass("no-scroll");
    showSuccess();
}

function showSuccess() {
    var NOT_VISIBLE_CLS = "not-visible";

    feedback.successForm = $(".successText");
    feedback.popupContent = $(".popup-content");
    feedback.popupContent.addClass(NOT_VISIBLE_CLS);
    feedback.successForm.removeClass(NOT_VISIBLE_CLS);

    setTimeout(function() {
        closeSendContent();
    }, 3000);
}