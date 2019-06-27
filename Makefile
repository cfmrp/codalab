all: competition/scoring_program.zip competition/training.zip competition/input.zip competition/evaluation.zip competition/companion.zip competition/sample.zip competition.zip submission.zip bad_submission.zip

competition/scoring_program.zip: scoring_program/* scoring_program/mtool
	cd scoring_program && zip -r ../competition/scoring_program.zip * && cd ..

scoring_program/mtool:
    cd scoring_program && git clone https://github.com/cfmrp/mtool && cd ..

competition/training.zip: mrp
	cd mrp/2019/training && zip -r ../../../competition/training.zip */*.mrp && cd ../../..

competition/input.zip: mrp
	cd mrp/2019/evaluation && zip -r ../../../competition/input.zip input.mrp && cd ../../..

competition/evaluation.zip: mrp
	cd mrp/2019/evaluation && zip -r ../../../competition/evaluation.zip */*.mrp && cd ../../..

competition/companion.zip: mrp
	cd mrp/2019/companion && zip -r ../../../competition/companion.zip *.mrp */*.conllu && cd ../../..

competition/sample.zip: mrp
	cd mrp/2019/sample && zip -r ../../../competition/sample.zip */*.mrp && cd ../../..

competition.zip: competition/* competition/scoring_program.zip competition/training.zip competition/evaluation.zip competition/companion.zip competition/sample.zip
	cd competition && zip -r  ../competition.zip * && cd ..

submission.zip: mrp
	mkdir -p submission && cd submission && cat ../mrp/2019/sample/*/*.mrp > sample.mrp && zip -r ../submission.zip * && cd ..

mrp:
    svn checkout http://svn.nlpl.eu/mrp

bad_submission.zip: scoring_program/mtool
	mkdir -p bad_submission && cd bad_submission && cat ../scoring_program/mtool/data/validate/*/*.mrp > bad.mrp && zip -r ../bad_submission.zip * && cd ..

clean:
	rm competition/scoring_program.zip competition/training.zip competition/input.zip competition/evaluation.zip competition/companion.zip competition/sample.zip competition.zip submission.zip bad_submission.zip