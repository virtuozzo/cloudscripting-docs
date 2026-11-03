/* Keyboard behavior for the pinned theme's existing tabs and mobile docs panel. */
;(function () {
    'use strict';

    function enhanceTabs() {
        document.querySelectorAll('[data-tabs-init]').forEach(function (container) {
            var tabs = Array.from(container.querySelectorAll('[role="tab"]'));
            var panels = Array.from(container.querySelectorAll('[role="tabpanel"]'));
            if (!tabs.length || tabs.length !== panels.length) return;

            function select(index) {
                tabs.forEach(function (tab, i) {
                    var active = i === index;
                    tab.setAttribute('aria-selected', String(active));
                    tab.tabIndex = active ? 0 : -1;
                    panels[i].hidden = !active;
                });
            }
            tabs.forEach(function (tab, index) {
                tab.id = container.id + '-tab-' + index;
                panels[index].id = container.id + '-panel-' + index;
                tab.setAttribute('aria-controls', panels[index].id);
                panels[index].setAttribute('aria-labelledby', tab.id);
                tab.addEventListener('click', function () { select(index); });
                tab.addEventListener('keydown', function (event) {
                    var next;
                    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
                    else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
                    else if (event.key === 'Home') next = 0;
                    else if (event.key === 'End') next = tabs.length - 1;
                    else return;
                    event.preventDefault();
                    tabs[next].focus();
                    tabs[next].click();
                });
            });
            select(Math.max(0, tabs.findIndex(function (tab) { return tab.getAttribute('aria-selected') === 'true'; })));
        });
    }

    function enhanceMobileMenu() {
        var toggle = document.querySelector('.sidebar-menu');
        var panel = document.querySelector('.aside');
        var close = document.querySelector('.hide-sidebar-menu');
        if (!toggle || !panel || !close) return;
        panel.id = panel.id || 'cs-docs-sidebar';
        toggle.setAttribute('role', 'button');
        toggle.tabIndex = 0;
        toggle.setAttribute('aria-controls', panel.id);
        close.setAttribute('role', 'button');
        close.setAttribute('aria-label', 'Close docs menu');
        close.tabIndex = 0;
        function sync() {
            toggle.setAttribute('aria-expanded', String(document.body.classList.contains('menu-open')));
        }
        function keyboardClick(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                event.currentTarget.click();
            }
        }
        toggle.addEventListener('keydown', keyboardClick);
        close.addEventListener('keydown', keyboardClick);
        toggle.addEventListener('click', function (event) {
            if (document.body.classList.contains('menu-open')) {
                event.stopPropagation();
                close.click();
            } else {
                window.setTimeout(function () {
                    var first = panel.querySelector('input, a[href], button, [tabindex="0"]');
                    if (first) first.focus();
                }, 0);
            }
        });
        close.addEventListener('click', function () { toggle.focus(); });
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && document.body.classList.contains('menu-open')) {
                event.preventDefault();
                close.click();
            }
        });
        new MutationObserver(sync).observe(document.body, {attributes: true, attributeFilter: ['class']});
        sync();
    }

    function enhanceMenuGroups() {
        var wrap = document.querySelector('.aside-menu-wrapp');
        if (!wrap) return;
        var sequence = 0;
        function sync() {
            wrap.querySelectorAll('li.has-children > .aside-menu-item').forEach(function (item) {
                // Fixed-open group headings are static text, not collapse buttons.
                if (item.parentElement.classList.contains('cs-menu-always-open')) return;
                // A real article link keeps its native navigation and modified clicks.
                if (item.querySelector('a[href]')) return;
                item.setAttribute('role', 'button');
                item.tabIndex = 0;
                item.setAttribute('aria-expanded', String(item.parentElement.classList.contains('expanded')));
                var children = item.parentElement.querySelector(':scope > ul');
                if (children) {
                    children.id = children.id || 'cs-docs-group-' + (++sequence);
                    item.setAttribute('aria-controls', children.id);
                }
            });
        }
        // Run before the shared theme's delegated toggle; real links stay native.
        wrap.addEventListener('click', function (event) {
            var item = event.target.closest('.aside-menu-item');
            if (item && item.parentElement.classList.contains('cs-menu-always-open') && !event.target.closest('a')) {
                event.stopPropagation();
            } else if (item && item.closest('.cs-menu-page-headings') &&
                       item.parentElement.classList.contains('has-children') && !event.target.closest('a')) {
                // Expand in place, as in the original docs. The shared theme
                // animates and auto-scrolls the last branch to its bottom.
                event.stopPropagation();
                item.parentElement.classList.toggle('expanded');
            }
        }, true);
        wrap.addEventListener('keydown', function (event) {
            var item = event.target.closest('.aside-menu-item[role="button"]');
            if (item && (event.key === 'Enter' || event.key === ' ')) {
                event.preventDefault();
                item.click();
            }
        });
        new MutationObserver(sync).observe(wrap, {subtree: true, childList: true, attributes: true, attributeFilter: ['class']});
        sync();
    }

    function enhancePageHeadings() {
        var items = Array.from(document.querySelectorAll('.cs-menu-page-headings [data-heading-id]'));
        if (!items.length) return;
        function sync() {
            var fragment = window.location.hash.slice(1);
            try { fragment = decodeURIComponent(fragment); } catch (error) {}
            items.forEach(function (item) {
                var target = item.querySelector('a') || item;
                if (item.getAttribute('data-heading-id') === fragment) {
                    target.setAttribute('aria-current', 'location');
                    var list = item.closest('.cs-menu-page-headings');
                    var parent = item.parentElement;
                    while (parent && list.contains(parent)) {
                        if (parent.classList.contains('has-children')) parent.classList.add('expanded');
                        parent = parent.parentElement.closest('li');
                    }
                } else target.removeAttribute('aria-current');
            });
        }
        document.querySelectorAll('.cs-menu-page-headings a').forEach(function (link) {
            link.addEventListener('click', function (event) {
                // Preserve native anchors, keyboard activation and modified clicks.
                if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
                if (document.body.classList.contains('menu-open')) {
                    var close = document.querySelector('.hide-sidebar-menu');
                    if (close) close.click();
                }
            });
        });
        window.addEventListener('hashchange', sync);
        sync();
    }

    function enhanceVersionPickers() {
        document.querySelectorAll('.versions').forEach(function (picker, index) {
            var toggle = picker.querySelector(':scope > .current');
            var links = picker.querySelector(':scope > .versions-list');
            if (!toggle || !links) return;
            links.id = links.id || 'cs-version-options-' + index;
            toggle.setAttribute('role', 'button');
            toggle.tabIndex = 0;
            toggle.setAttribute('aria-label', 'Choose documentation version, current label ' + toggle.textContent.trim());
            toggle.setAttribute('aria-controls', links.id);
            function sync() { toggle.setAttribute('aria-expanded', String(picker.classList.contains('active'))); }
            toggle.addEventListener('keydown', function (event) {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    toggle.click();
                    if (picker.classList.contains('active')) {
                        var first = links.querySelector('a[aria-current="true"], a[href]');
                        if (first) first.focus();
                    }
                }
            });
            picker.addEventListener('keydown', function (event) {
                if (event.key === 'Escape' && picker.classList.contains('active')) {
                    event.preventDefault();
                    event.stopPropagation();
                    picker.classList.remove('active');
                    toggle.focus();
                }
            });
            new MutationObserver(sync).observe(picker, {attributes: true, attributeFilter: ['class']});
            sync();
        });
    }

    function ready() { enhanceTabs(); enhanceMobileMenu(); enhanceMenuGroups(); enhancePageHeadings(); enhanceVersionPickers(); }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
    else ready();
}());
