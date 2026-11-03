/* Presentation only. The existing tab/copy handlers and code bytes stay intact. */
;(function () {
    'use strict';

    function enhanceCodeBlocks() {
        document.querySelectorAll('[data-tabs-init]').forEach(function (container) {
            var panels = Array.from(container.querySelectorAll(':scope > .tabs-content > .tab-panel'));
            if (panels.length && panels.every(function (panel) {
                return panel.children.length === 1 && panel.firstElementChild.classList.contains('code-block');
            })) container.classList.add('cs-code-tabs');
        });

        var updates = new Map();
        var observer = window.ResizeObserver && new ResizeObserver(function (entries) {
            entries.forEach(function (entry) { updates.get(entry.target)(); });
        });

        document.querySelectorAll('.code-block').forEach(function (block) {
            var region = block.querySelector('.highlight');
            var code = region && region.querySelector('pre code');
            if (!region || !code || block.classList.contains('cs-code-viewer')) return;
            block.classList.add('cs-code-viewer');
            region.setAttribute('role', 'region');
            region.setAttribute('aria-label', (code.dataset.lang || 'Plain text').toUpperCase() + ' code example');

            function update() {
                if (!region.clientHeight) return; // Re-measured when an inactive tab becomes visible.
                region.tabIndex = region.scrollWidth > region.clientWidth + 1 ? 0 : -1;
                // Avoid two consecutive focus stops for the same scrolling surface.
                region.querySelectorAll('pre[tabindex]').forEach(function (pre) { pre.tabIndex = -1; });
            }

            updates.set(region, update);
            if (observer) observer.observe(region);
            update();
        });

        // ResizeObserver handles viewport changes and panels becoming visible.
        // Keep horizontal scrolling keyboard-accessible without it as well.
        if (!observer) {
            window.addEventListener('resize', function () { updates.forEach(function (update) { update(); }); });
            document.addEventListener('click', function (event) {
                if (event.target.closest('[role="tab"]')) {
                    window.requestAnimationFrame(function () { updates.forEach(function (update) { update(); }); });
                }
            });
        }
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enhanceCodeBlocks);
    else enhanceCodeBlocks();
}());
