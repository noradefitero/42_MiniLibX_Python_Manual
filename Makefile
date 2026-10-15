SRC_DIR      := src
DIST_DIR     := dist
TEMPLATE_DIR := $(SRC_DIR)/template

SRC          := \
                $(SRC_DIR)/manual.md

TEMPLATE_README_MD  := $(TEMPLATE_DIR)/readme_md.tex
TEMPLATE_MD  := $(TEMPLATE_DIR)/md.tex
TEMPLATE_PDF := $(TEMPLATE_DIR)/pdf.tex

FILTER_FIGURES := $(TEMPLATE_DIR)/figure-captions.lua
FILTER_ALERTS  := $(TEMPLATE_DIR)/alerts.lua

MD_FILES     := $(patsubst $(SRC_DIR)/%.md,$(DIST_DIR)/%.md,$(SRC))
PDF_FILES    := $(patsubst $(SRC_DIR)/%.md,$(DIST_DIR)/%.pdf,$(SRC))

all: markdown pdf readme
.PHONY: all

markdown: $(MD_FILES)
.PHONY: markdown

pdf: $(PDF_FILES)
.PHONY: pdf

readme: README.md
.PHONY: readme

README.md: $(SRC_DIR)/manual.md $(TEMPLATE_README_MD) $(FILTER_FIGURES)
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_README_MD) -f gfm -t gfm --toc --lua-filter $(FILTER_FIGURES) $< -o $@

$(DIST_DIR)/%.md: $(SRC_DIR)/%.md $(TEMPLATE_MD) $(FILTER_FIGURES)
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_MD) -f gfm -t gfm --toc --lua-filter $(FILTER_FIGURES) $< -o $@

$(DIST_DIR)/%.pdf: $(SRC_DIR)/%.md $(TEMPLATE_PDF) $(FILTER_ALERTS)
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_PDF) -f markdown+alerts --lua-filter $(FILTER_ALERTS) $< -o $@

clean:
	rm -rf $(DIST_DIR) README.md
.PHONY: clean

re: clean all
.PHONY: re

init:
	@uv run --with pre-commit pre-commit install
