build:
	docker build -t fit-lecture-indexer .

run:
	docker run -it --rm --name fit-lecture-indexer -v $PWD/video:/usr/app/video -v $PWD/output:/usr/app/output fit-lecture-indexer /bin/bash
