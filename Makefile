
all: unittests

unittests:
	cd tests; python test_all.py

tarball:
	tar --exclude=.svn --exclude=*.pyc --exclude=.project --exclude=.pydevproject -zcSvf wxscheduler.tar.gz .