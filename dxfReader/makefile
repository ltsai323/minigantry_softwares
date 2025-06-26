
.PHONY: help ## print help by default


check_defined = \
    $(strip $(foreach 1,$1, \
    $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
    $(error Undefined $1$(if $2, ($2))))

check_shell_var_defined = \
  	$(if $(shell [ -z "$${$1}" ] && echo undefined), \
	$(error Shell variable $1 is undefined), \
	$(info Shell variable $1 is set))


step1_convertdxf: ## convert a dxf file to point [dxfFILE=V3-LD-SemiLeft3_solidworks.dxf]
	$(call check_defined, dxfFILE)
	python3 python/dxfReader.py $(dxfFILE)
step2_sortpoint: ## convert step1 text file to sorted points
	python3 python/sortedPoint.py step1_dxfReader.txt  0
step2_sortpoint_180rotate: ## convert step1 text file to sorted points
	python3 python/sortedPoint.py step1_dxfReader.txt  1
step3_checkpoints: ## checking [iFILE=step2_sortedPoints.LabCoordinate.txt]
	$(call check_defined, iFILE)
	python3 python/checkpoints.py $(iFILE)


clean: ## clean output files
	/bin/rm step*.png step*.txt

$(OUTPUT_DIR):
	$(call check_defined, jobname)
	@echo Folder not found: Initialize folder $(OUTPUT_DIR)
	mkdir -p $@

IN_ARGS = [opts]

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[32m<command>\033[0m $(IN_ARGS)\n\nCommands:\n\033[36m\033[0m\n"} /^[0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
