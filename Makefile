INSTALLDIR=${HOME}/.ts

install: clone mod

mod:
	chmod +x "${INSTALLDIR}/ts"
	chmod +x "${INSTALLDIR}/start"
	chmod +x "${INSTALLDIR}/stop"
	chmod +x "${INSTALLDIR}/log"

clone: ${INSTALLDIR}
	git clone . $<

.PHONY: install mod clone

