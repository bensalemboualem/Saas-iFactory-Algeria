# DzirVideo - YouTube Shorts Automation
.PHONY: help build start stop restart logs test generate upload clean

help:  ## Show this help
	@echo "DzirVideo - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build:  ## Build Docker image
	docker-compose build

start:  ## Start services
	docker-compose up -d
	@echo "API running at http://localhost:8200"

stop:  ## Stop services
	docker-compose down

restart:  ## Restart services
	$(MAKE) stop
	$(MAKE) start

logs:  ## View logs
	docker-compose logs -f

test:  ## Run tests
	docker-compose exec dzirvideo python -m pytest tests/

generate:  ## Generate video from script (usage: make generate SCRIPT=scripts/01.md TITLE="My Video")
	@if [ -z "$(SCRIPT)" ] || [ -z "$(TITLE)" ]; then \
		echo "Usage: make generate SCRIPT=scripts/01.md TITLE=\"My Video Title\""; \
		exit 1; \
	fi
	@echo "Generating video: $(TITLE)"
	@curl -X POST http://localhost:8200/generate/file \
		-F "script_file=@$(SCRIPT)" \
		-F "title=$(TITLE)" \
		-F "description=$(DESC)" \
		-F "tags=$(TAGS)" \
		-F "publish=$(PUBLISH)" \
		| jq .

upload:  ## Upload existing video to YouTube (usage: make upload VIDEO=output/videos/test.mp4 TITLE="My Video")
	@if [ -z "$(VIDEO)" ] || [ -z "$(TITLE)" ]; then \
		echo "Usage: make upload VIDEO=output/videos/test.mp4 TITLE=\"My Video Title\""; \
		exit 1; \
	fi
	@echo "Uploading video: $(VIDEO)"
	@curl -X POST http://localhost:8200/upload \
		-F "video=@$(VIDEO)" \
		-F "title=$(TITLE)" \
		| jq .

clean:  ## Clean output files
	rm -rf output/videos/*.mp4
	rm -rf output/audio/*.mp3
	rm -rf output/subtitles/*.srt

status:  ## Check pipeline status
	@curl -s http://localhost:8200/status | jq .

# Quick commands
run:  ## Quick generate (SCRIPT, TITLE, PUBLISH=false)
	@$(MAKE) generate SCRIPT=$(SCRIPT) TITLE="$(TITLE)" PUBLISH=$(or $(PUBLISH),false)

publish:  ## Quick generate + publish (SCRIPT, TITLE)
	@$(MAKE) generate SCRIPT=$(SCRIPT) TITLE="$(TITLE)" PUBLISH=true
