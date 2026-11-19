.DEFAULT_GOAL := help
MANIFEST ?= manifests/current.yaml

.PHONY: help workspace status contracts check structure drift integrate validate

help:  ## Liste les cibles
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "%-12s %s\n", $$1, $$2}'

workspace:  ## Monte workspace/ aux SHA du manifeste (MANIFEST=…)
	uv run scripts/workspace $(MANIFEST)

status:  ## Ce qui est monté dans workspace/, et à quel SHA
	uv run scripts/workspace $(MANIFEST) --status

contracts:  ## Régénère les contrats issus du code, depuis workspace/
	uv run scripts/extract-contracts

structure:  ## Validations croisées (sans les composants)
	uv run scripts/checks/structure

drift:  ## Dérive des contrats (workspace) et des SHA (dépôts locaux)
	uv run scripts/checks/drift

check: structure drift  ## structure + dérive

validate:  ## Ce que la CI lance sur chaque PR du home repo
	ci/validate

integrate:  ## Intègre un manifeste : portes, contrats (MANIFEST=…)
	uv run ci/integrate $(MANIFEST)
