DIST_DIR     := dist
TEMPLATE_DIR := src/template

SRC          := src/manual.md

TEMPLATE_README_MD  := $(TEMPLATE_DIR)/readme_md.tex
TEMPLATE_MD  := $(TEMPLATE_DIR)/md.tex
TEMPLATE_PDF := $(TEMPLATE_DIR)/pdf.tex
TEMPLATE_HTML := $(TEMPLATE_DIR)/web/index.html
TEMPLATE_CSS := $(TEMPLATE_DIR)/web/style.css
TEMPLATE_YETI := $(TEMPLATE_DIR)/web/yeti.min.css

FILTER_FIGURES := $(TEMPLATE_DIR)/figure-captions.lua
FILTER_ALERTS  := $(TEMPLATE_DIR)/alerts.lua
FILTER_YETI    := $(TEMPLATE_HTML:index.html=yeti.lua)
FILTER_TABLES  := $(TEMPLATE_DIR)/table-widths.lua
FILTER_CENTER  := $(TEMPLATE_DIR)/figure-center.lua

MINIFY_HTML    := uv run --with minify-html python scripts/minify-web.py

MD_FILES     := $(patsubst src/%.md,$(DIST_DIR)/%.md,$(SRC))
PDF_FILES    := $(patsubst src/%.md,$(DIST_DIR)/%.pdf,$(SRC))
WEB_FILE	:= $(DIST_DIR)/web/index.html

all: markdown pdf readme web
.PHONY: all

markdown: $(MD_FILES)
.PHONY: markdown

pdf: $(PDF_FILES)
.PHONY: pdf

readme: README.md
.PHONY: readme

web: $(WEB_FILE)
.PHONY: web

README.md: src/manual.md $(TEMPLATE_README_MD) $(FILTER_FIGURES)
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_README_MD) -f gfm -t gfm --toc --lua-filter $(FILTER_FIGURES) $< -o $@

$(DIST_DIR)/%.md: src/manual.md $(TEMPLATE_MD) $(FILTER_FIGURES)
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_MD) -f gfm -t gfm --toc --lua-filter $(FILTER_FIGURES) $< -o $@

$(DIST_DIR)/%.pdf: src/manual.md $(TEMPLATE_PDF) $(FILTER_ALERTS) $(FILTER_TABLES) $(FILTER_CENTER)
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_PDF) -f gfm --lua-filter $(FILTER_ALERTS) --lua-filter $(FILTER_FIGURES) --lua-filter $(FILTER_TABLES) --lua-filter $(FILTER_CENTER) $< -o $@

$(DIST_DIR)/%.html: src/manual.md $(TEMPLATE_HTML) $(TEMPLATE_YETI) $(TEMPLATE_CSS) $(FILTER_YETI)
	mkdir -p $(dir $@)
	pandoc \
	        -f gfm \
	        -t html \
			--toc \
			--toc-depth=2 \
	        --template $(TEMPLATE_HTML) \
	        --lua-filter $(FILTER_FIGURES) \
	        --lua-filter $(FILTER_YETI) \
	        --css yeti.min.css \
	        --css style.css \
	        --metadata author="Nora de Fitero Teijeira" \
			$< -o $@
	cp $(TEMPLATE_YETI) $(DIST_DIR)/web/yeti.min.css
	cp $(TEMPLATE_CSS) $(DIST_DIR)/web/style.css
	rm -rf $(DIST_DIR)/web/media && cp -R media $(DIST_DIR)/web/media
	$(MINIFY_HTML) $(DIST_DIR)/web/*html $(DIST_DIR)/web/*css

clean:
	rm -rf $(DIST_DIR) README.md
.PHONY: clean

re: clean all
.PHONY: re

init:
	uv sync
	uv run pre-commit install
