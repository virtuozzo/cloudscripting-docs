"""Build real fixture sites; run from repository root with the pinned Hugo in PATH."""
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).resolve().parent


def verify():
    # Missing configuration, flattened permalinks, draft-enabled builds, invisible
    # menu groups, broken asset plumbing, and wrong product metadata must fail.
    assert (ROOT / "config.yaml").is_file(), "Missing pinned Hugo config.yaml"
    version = subprocess.check_output(["hugo", "version"], text=True)
    assert "v0.124.1" in version and "+extended" in version, version
    for base in ("https://www.virtuozzo.com/cloudscripting-docs/", "https://example.test/docs/8.14.3/"):
        with tempfile.TemporaryDirectory(prefix="cloudscripting-foundation-") as temp:
            out = Path(temp) / "public"
            command = ["hugo", "--source", str(ROOT), "--config",
                       str(ROOT / "config.yaml"),
                       "--contentDir", str(FIXTURE / "content"), "--destination", str(out),
                       "--baseURL", base, "--cacheDir", str(Path(temp) / "cache")]
            subprocess.run(command, check=True)
            home = (out / "index.html").read_text()
            article = (out / "creating-manifest/actions/index.html").read_text()
            assert not (out / "actions/index.html").exists(), "Nested article flattened"
            assert not (out / "private-draft/index.html").exists(), "Draft published"
            assert not (out / "creating-manifest/index.html").exists(), "Grouping section published"
            for text in ("GETTING STARTED", "Creating Manifest", "Actions fixture", "Quick Start fixture"):
                assert text in article, f"Menu entry invisible: {text}"
            assert f'<link rel="canonical" href="{base}creating-manifest/actions/">' in article, "Nested canonical URL lost prefix"
            assert base + "images/vz_logo.svg" in article, "Logo URL lost prefix"
            assert (out / "images/vz_logo.svg").is_file(), "Branded logo not copied"
            assert 'id="fixture-html"' in article, "Raw HTML dropped"
            assert "Documentation Portal for Cloud Scripting" in home
            assert "Cloud Scripting" in article
            assert "https://www.virtuozzo.com/cloudscripting-docs/#software" in article, "Product schema missing"
            assert (out / "404.html").is_file(), "404 artifact missing"
            assert (out / "css/styles.css").is_file(), "Extended Sass stylesheet missing"
            index = json.loads((out / "index.json").read_text())
            assert {item["permalink"] for item in index} == {base, base + "creating-manifest/actions/", base + "quick-start/"}, "Home JSON routes incorrect"
            assert "Unapproved draft" not in json.dumps(index), "Draft indexed"
            for token in ("UA-89532314-1", "google-analytics.com/analytics.js"):
                assert token not in home + article, f"Unapproved analytics rendered: {token}"
            for token in ("GTM-W9PSVPL", "otSDKStub.js"):
                assert (token in home + article) == base.startswith("https://www.virtuozzo.com/"), f"Corporate analytics host gate incorrect: {token}"
            print("PASS", base, "nested route, drafts, menu groups, branding, raw HTML, Sass, JSON, analytics")


if __name__ == "__main__":
    verify()
