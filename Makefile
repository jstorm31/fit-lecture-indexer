build:
	docker build -t fit-lecture-indexer .

run:
	docker run -it --rm --name fit-lecture-indexer -v $(pwd)/video:/usr/app/video -v $(pwd)/src:/usr/app/src fit-lecture-indexer /bin/bash
