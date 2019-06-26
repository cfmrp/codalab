all: competition/scoring_program.zip competition/training09.tgz competition/evaluation09.tgz competition/companion.tgz competition/sample.tgz competition.zip submission.zip

competition/scoring_program.zip: scoring_program/* scoring_program/mtool
	cd scoring_program && zip -r ../competition/scoring_program.zip * && cd ..

scoring_program/mtool:
    cd scoring_program && git clone https://github.com/cfmrp/mtool

competition/training09.tgz: mrp
	cd mrp/2019/training && make release && cd ../../.. && cp mrp/2019/training09.tgz competition/

competition/evaluation09.tgz: mrp
	cd mrp/2019/evaluation && make release && cd ../../.. && cp mrp/2019/evaluation09.tgz competition/

competition/companion.tgz: mrp
	cd mrp/2019/companion && make release && cd ../../.. && cp mrp/2019/public/companion.tgz competition/

competition/sample.tgz: mrp
	cd mrp/2019/sample && make release && cd ../../.. && cp mrp/2019/public/sample.tgz competition/

competition.zip: competition/* competition/scoring_program.zip competition/training09.tgz competition/evaluation09.tgz competition/companion.tgz competition/sample.tgz
	cd competition && zip -r  ../competition.zip * && cd ..

submission.zip: competition/sample.tgz
	mkdir -p sample && cd sample && tar xvzf ../competition/sample.tgz && zip -r ../submission.zip * && cd ..

mrp:
    svn checkout http://svn.nlpl.eu/mrp

clean:
	rm competition/scoring_program.zip competition/training09.tgz competition/evaluation09.tgz competition/companion.tgz competition/sample.tgz competition.zip submission.zip