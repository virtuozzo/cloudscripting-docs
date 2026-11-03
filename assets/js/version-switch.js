// Based on pinned docs-theme 91b3863e; retain same-article query state.
/*
 * Version switcher: open the same article in the other version.
 * The links in .versions-list point to each version's home (no redirects or 404s for crawlers).
 * On click we try, in order: the same path in the target version, the target version's home in the
 * current language, then the plain link. Each candidate is checked with a HEAD request; aliases and
 * server redirects are followed. Modified clicks (new tab etc.) and errors fall back to the link.
 */
(function () {
    function exists(url) {
        return fetch(url, { method: 'HEAD', credentials: 'same-origin' })
            .then(function (r) { return r.ok ? r.url || url : null; })
            .catch(function () { return null; });
    }

    document.addEventListener('click', function (e) {
        var a = e.target.closest && e.target.closest('.versions-list a[data-vs-from]');
        if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        if (a.getAttribute('aria-current') === 'true') return;
        if (!window.fetch || !window.URL) return;

        var target = a.href;
        var fromPath = new URL(a.getAttribute('data-vs-from'), location.href).pathname;
        var path = location.pathname;
        if (path.indexOf(fromPath) !== 0) return;
        var rel = path.slice(fromPath.length);
        var lang = a.getAttribute('data-vs-lang') || '';

        var candidates = [];
        if (rel && rel !== lang) candidates.push(target + rel + location.search + location.hash);
        if (lang) candidates.push(target + lang);
        if (!candidates.length) return;

        e.preventDefault();
        (function next(i) {
            if (i >= candidates.length) { location.href = target; return; }
            exists(candidates[i].split('#')[0]).then(function (url) {
                if (url) location.href = url + (i === 0 ? location.hash : '');
                else next(i + 1);
            });
        })(0);
    });
})();
