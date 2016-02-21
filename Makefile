INSTALLDIR=.
install: mod

mod:
	chmod +x "${INSTALLDIR}/ts"

.PHONY: install mod 

