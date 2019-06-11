var App = {};
App.error = {};
App.error.Report = function() {
    var me = this,
        BODY = "body",
        NOT_VISIBLE_CLS = "not-visible",
        DISABLE = "disable",
        oSelection,
        sSelection,
        oReportEls = {};

    this.initElements = function() {
        oReportEls.body = oBody = $(BODY);
        oReportEls.gridBody = oBody.children('.wy-grid-for-nav');
        oReportEls.wrapper = oWrapper = $(".wrapper-send-report");
        oReportEls.popupContent = oWrapper.children(":first");
        oReportEls.description = oDescription = oWrapper.find(".popup-description");
        oReportEls.textarea = oTextArea = oReportEls.popupContent.find(".comment");
        oReportEls.note = oReportEls.popupContent.find(".rst-content");
        oReportEls.selectedText = oDescription.find(".selected .text");
        oReportEls.selectedParent= "";
        oReportEls.sendBtn = oSendBtn = oReportEls.popupContent.find('.actions .btn');
        oReportEls.successForm = oReportEls.popupContent.find(".successText");
        oReportEls.username = oReportEls.popupContent.find(".name .input");

        oReportEls.textarea.keyup(me.enableSendBtn).focusout(me.enableSendBtn);

        oReportEls.body.keypress(function (e) {
            if (e.ctrlKey && (e.keyCode == 10 || e.keyCode == 13)) {
                me.openReportForm();
            }
        });

        $("a.bug-found").on('click', me.openReportForm);

        oReportEls.body.keyup(function(e) {
            if (e.keyCode == 27) {
                oReportEls.wrapper.addClass(NOT_VISIBLE_CLS);
                oReportEls.gridBody.css({'overflow': "scroll"});
            }
        });

        oReportEls.body.on('click', function(event) {
            if (event.target.className == "wrapper-send-report" &&
                !oReportEls.wrapper.hasClass(NOT_VISIBLE_CLS) &&
                oReportEls.popupContent.hasClass(NOT_VISIBLE_CLS) &&
                !oReportEls.successForm.hasClass(NOT_VISIBLE_CLS) &&
                $('.wy-body-for-nav').has(event.target).length) {
                me.closeSendContent();
            }
        });
    };

    this.enableSendBtn = function() {
        if (this.value && !this.value.trim()) {
            oReportEls.sendBtn.addClass(DISABLE);
        } else {
            oReportEls.sendBtn.removeClass(DISABLE);
        }
    };

    this.preventDefaultEvent = function(e) {
        if (!oReportEls.wrapper.hasClass(NOT_VISIBLE_CLS) && e.target.className == "wrapper-send-report"){
            e = e || window.event;
            if (e.preventDefault)
                e.preventDefault();
            e.returnValue = false;
        }
    };

    this.openReportForm = function() {
        if (!oReportEls.wrapper.hasClass(NOT_VISIBLE_CLS)) return;

        oReportEls.popupContent.removeClass(NOT_VISIBLE_CLS);
        oSelection = window.getSelection();
        sSelection = oSelection.toString() || "";
        oReportEls.selectedParent = oSelection.anchorNode;
        oReportEls.wrapper.removeClass(NOT_VISIBLE_CLS);
        oReportEls.gridBody.css({'overflow': "hidden"});

        if (oReportEls.username.val()) {
            oReportEls.textarea.focus();
        } else {
            oReportEls.username.focus();
        }

        if (sSelection) {
            oReportEls.sendBtn.removeClass(DISABLE);
            oReportEls.description.removeClass(NOT_VISIBLE_CLS);
            oReportEls.selectedText.text(sSelection);
            oReportEls.note.addClass(NOT_VISIBLE_CLS);
        } else {
            oReportEls.note.removeClass(NOT_VISIBLE_CLS);
            oReportEls.description.addClass(NOT_VISIBLE_CLS);
        }

        me.setCenterForm();

        if (!oReportEls.textarea.val()) {
            oReportEls.sendBtn.addClass(DISABLE);
        }

        return false;
    };

    this.setCenterForm = function() {
        var nValue;

        nValue = (window.innerHeight - oReportEls.popupContent.height()) / 2;
        oReportEls.popupContent.css({"margin-top": nValue + "px"})
    };

    this.closeSendContent = function() {
        oReportEls.successForm.addClass(NOT_VISIBLE_CLS);
        oReportEls.wrapper.addClass(NOT_VISIBLE_CLS);
        oReportEls.gridBody.css({'overflow': "scroll"});
    };

    this.showSuccess = function() {
        var NOT_VISIBLE_CLS = "not-visible";

        oReportEls.successForm = $(".successText");
        oReportEls.popupContent = $(".popup-content");
        oReportEls.popupContent.addClass(NOT_VISIBLE_CLS);
        oReportEls.successForm.removeClass(NOT_VISIBLE_CLS);

        setTimeout(function() {
            closeSendContent();
        }, 3000);
    };

    this.sendIssue = function() {
        var xhr = new XMLHttpRequest(),
            url = window.location.protocol + "//" + window.location.hostname + "/issue_report.php",
            sComment = oReportEls.textarea.val() || "",
            sSelected = oReportEls.selectedText.text() || "",
            oSelectedAnchorNode = oReportEls.selectedParent,
            sSelectedParent = oSelectedAnchorNode.parentElement,
            sUserName = oReportEls.username.val() || "",
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
        nChildIndex = oChildren.index(oReportEls.selectedParent.parentElement);

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
        oReportEls.textarea.val("");
        oReportEls.gridBody.removeClass("no-scroll");
        me.showSuccess();
    };
};

(function() {
    var oReport = new App.error.Report();

    $("body").ready(function () {
        oReport.initElements();

        window.addEventListener('DOMMouseScroll', oReport.preventDefaultEvent, false);
        window.onwheel = oReport.preventDefaultEvent; // modern standard
        window.onmousewheel = document.onmousewheel = oReport.preventDefaultEvent; // older browsers, IE
        window.ontouchmove  = oReport.preventDefaultEvent;
    });
})();