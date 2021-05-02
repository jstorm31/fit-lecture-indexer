build:
	docker build -t fit-lecture-indexer .

run:
	docker run -it --rm --name fit-lecture-indexer -v video:/usr/app/video -v src:/usr/app/src fit-lecture-indexer /bin/bash
