SRC_DIR      := src
DIST_DIR     := dist

SRC          := \
                $(SRC_DIR)/manual.md

TEMPLATE_README_MD  := $(SRC_DIR)/template/readme_md.tex
TEMPLATE_MD  := $(SRC_DIR)/template/md.tex
TEMPLATE_PDF := $(SRC_DIR)/template/pdf.tex

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

README.md: $(SRC_DIR)/manual.md
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_README_MD) -t gfm --shift-heading-level-by=1 --toc $< -o $@

$(DIST_DIR)/%.md: $(SRC_DIR)/%.md
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_MD) -t gfm --shift-heading-level-by=1 --toc $< -o $@

$(DIST_DIR)/%.pdf: $(SRC_DIR)/%.md
	mkdir -p $(dir $@)
	pandoc --template $(TEMPLATE_PDF) $< -o $@

clean:
	rm -rf $(DIST_DIR) README.md
.PHONY: clean

re: clean all
.PHONY: re

init:
	@uv run --with pre-commit pre-commit install
