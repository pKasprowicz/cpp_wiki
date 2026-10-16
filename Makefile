# Thin wrapper: every target calls scripts/build-site.sh, the same script CI runs.
# No make? Run the script directly: bash scripts/build-site.sh {check|build|serve|clean}

SITE_SCRIPT := scripts/build-site.sh

.PHONY: site-check site-build site-serve site-clean

# Wiki lint + broken-wikilink check (needs only Python 3.9+).
site-check:
	bash $(SITE_SCRIPT) check

# Build the static site into public/ (needs Node >= 22; Quartz is fetched into .quartz-cache/).
site-build:
	bash $(SITE_SCRIPT) build

# Local preview with hot reload at http://localhost:8080/ (override with PORT=...).
site-serve:
	bash $(SITE_SCRIPT) serve

# Remove public/ and .quartz-cache/.
site-clean:
	bash $(SITE_SCRIPT) clean
