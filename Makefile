# -*- makefile -*- 

# For a description of GNU style Makefiles see:
#
# http://www.gnu.org/s/make/

default:
	@echo "  Make rules for the research tools class directory"
	@echo
	@echo "	update - do a mercurial pull and update"
	@echo "	clean  - remove generated files like html from org files"

update:
	hg pull
	hg update

clean:
	(cd class && rm -f *.html)

