INSTALLDIR=${HOME}/.ts

install: clone mod

mod:
	chmod +x "${INSTALLDIR}/ts"

clone: ${INSTALLDIR}
	git clone . $<

.PHONY: install mod clone

